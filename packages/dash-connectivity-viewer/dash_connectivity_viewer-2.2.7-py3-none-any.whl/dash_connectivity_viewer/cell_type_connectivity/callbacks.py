import datetime
import pytz
import numpy as np
from functools import partial
import traceback

from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State

from .config import TypedConnectivityConfig
from ..common.link_utilities import (
    generate_statebuilder,
    generate_statebuilder_pre,
    generate_statebuilder_post,
    generate_statebuider_syn_grouped,
    generate_statebuilder_syn_cell_types,
    EMPTY_INFO_CACHE,
    MAX_URL_LENGTH,
    make_url_robust,
    aligned_volume,
    get_viewer_site_from_target,
)
from ..common.dash_url_helper import _COMPONENT_ID_TYPE
from ..common.lookup_utilities import (
    get_type_tables,
    make_client,
    get_version_options,
)
from ..common.schema_utils import get_table_info
from ..common.dataframe_utilities import (
    stringify_root_ids,
    stringify_list,
    rehydrate_dataframe,
    rebuild_synapse_dataframe,
)
from .neuron_data_cortex import NeuronDataCortex as NeuronData
from .neuron_data_cortex import ALLOW_COLUMN_TYPES_DISCRETE
from .cortex_panels import *

try:
    from loguru import logger
    import time
except:
    logger = None


InputDatastack = Input({"id_inner": "datastack", "type": _COMPONENT_ID_TYPE}, "value")
OutputDatastack = Output({"id_inner": "datastack", "type": _COMPONENT_ID_TYPE}, "value")

StateRootID = State({"id_inner": "anno-id", "type": _COMPONENT_ID_TYPE}, "value")
StateCellTypeTable = State(
    {"id_inner": "cell-type-table-dropdown", "type": _COMPONENT_ID_TYPE},
    "value",
)
OutputCellTypeMenuOptions = Output(
    {"id_inner": "cell-type-table-dropdown", "type": _COMPONENT_ID_TYPE},
    "options",
)
OutputCellTypeValue = Output(
    {"id_inner": "cell-type-table-dropdown", "type": _COMPONENT_ID_TYPE},
    "value",
)

InputMaterializationVersion = Input(
    {"id_inner": "mat-version", "type": _COMPONENT_ID_TYPE}, "value"
)
StateMaterializationVersion = State(
    {"id_inner": "mat-version", "type": _COMPONENT_ID_TYPE}, "value"
)
OutputMaterializeOptions = Output(
    {"id_inner": "mat-version", "type": _COMPONENT_ID_TYPE}, "options"
)
OutputMaterializeValue = Output(
    {"id_inner": "mat-version", "type": _COMPONENT_ID_TYPE}, "value"
)

StateAnnoType = State({"id_inner": "id-type", "type": _COMPONENT_ID_TYPE}, "value")
StateLiveQuery = State(
    {"id_inner": "live-query-toggle", "type": _COMPONENT_ID_TYPE}, "value"
)
StateLinkGroupValue = State("group-by", "value")

OutputLiveQueryToggle = Output(
    {"id_inner": "live-query-toggle", "type": _COMPONENT_ID_TYPE},
    "options",
)
OutputLiveQueryValue = Output(
    {"id_inner": "live-query-toggle", "type": _COMPONENT_ID_TYPE}, "value"
)


def allowed_action_trigger(ctx, allowed_buttons):
    if not ctx.triggered:
        return False
    trigger_src = ctx.triggered[0]["prop_id"].split(".")[0]
    return trigger_src in allowed_buttons


def generic_syn_link_generation(
    sb_function,
    rows,
    info_cache,
    datastack,
    config,
    link_text,
    item_name="synapses",
):
    if rows is None or len(rows) == 0:
        return html.Div(f"No {item_name} to show")
    else:
        syn_df = rehydrate_dataframe(rows, config.syn_pt_position_split)
        sb = sb_function(info_cache)
    try:
        url = make_url_robust(
            syn_df.sort_values(by=config.num_syn_col, ascending=False),
            sb,
            datastack,
            config,
        )
    except Exception as e:
        return html.Div(str(e))

    return html.A(link_text, href=url, target="_blank", style={"font-size": "20px"})


def make_violin_plot(ndat, height=350):
    if ndat is None:
        return html.Div("")

    violin = violin_fig(ndat, height=height)
    contents = [
        html.H5("Input/Output Depth", className="card-title"),
        dcc.Graph(
            figure=violin,
            style={
                "margin-left": "5rem",
                "margin-right": "5rem",
                "width": "auto",
                "height": "25rem",
            },
        ),
    ]
    return contents


def make_ct_plots(rows, config, aligned_volume, color_column, table_values):
    if rows is None:
        return html.Div(""), html.Div("")
    if len(rows) == 0:
        return html.Div(""), html.Div("")

    df = rebuild_synapse_dataframe(
        rows,
        config,
        aligned_volume,
        value_cols=[color_column],
    )
    if color_column in table_values:
        df[color_column] = df[color_column].astype(
            pd.CategoricalDtype(
                categories=sorted(table_values[color_column])
                + [config.null_cell_type_label],
                ordered=True,
            )
        )

    if color_column == "":
        color_column = None

    if config.show_depth_plots:
        scatter_contents = make_scatter_div(
            df.copy(), config, color_column, width=450, height=350
        )
    else:
        scatter_contents = html.Div("")
    bar_contents = make_bar_div(df.copy(), config, color_column, width=450, height=350)

    return scatter_contents, bar_contents


def make_scatter_div(
    df,
    config,
    color_column,
    width=450,
    height=350,
):
    scatter_fig = scatter_fig_df(df, config, color_column, width, height)
    contents = [
        html.H5("Synapse/Target Soma Depth", className="card-title"),
        dcc.Graph(
            figure=scatter_fig,
            style={"height": "100%", "width": "auto"},
        ),
    ]
    return contents


def make_bar_div(df, config, color_column, width=450, height=350):
    if color_column is None:
        contents = [
            html.H4(
                "Select value column for bar chart",
                style={"text-align": "center", "vertical-align": "middle"},
            ),
        ]
    else:
        bar_fig = bar_fig_df(df, config, color_column)
        contents = [
            html.H5("Target Distribution", style={"text-align": "center"}),
            dcc.Graph(figure=bar_fig, style={"width": "auto", "height": "100%"}),
        ]
    return contents


def register_callbacks(app, config):
    c = TypedConnectivityConfig(config)

    @app.callback(
        Output("data-table", "selected_rows"),
        Input("reset-selection", "n_clicks"),
        Input("connectivity-tab", "value"),
    )
    def reset_selection(n_clicks, tab_value):
        return []

    @app.callback(
        Output("header-bar", "children"),
        InputDatastack,
    )
    def set_header(datastack):
        return html.H3(
            f"Typed Connectivity Viewer — {datastack}",
            className="bg-primary text-white p-2 mb-2 text-center",
        )

    @app.callback(
        OutputMaterializeOptions,
        OutputMaterializeValue,
        InputDatastack,
    )
    def get_materialization_versions(
        datastack_name,
    ):
        # Produce ordered list of materialization versions to choose from
        client = make_client(datastack_name, c.server_address)
        version_options, default_value = get_version_options(
            client, c.disallow_live_query
        )
        return version_options, default_value

    @app.callback(
        Output("data-table", "columns"),
        Output("group-by", "options"),
        Output("unique-table-values", "data"),
        Input("submit-button", "n_clicks"),
        InputDatastack,
        StateCellTypeTable,
    )
    def define_table_columns(_, datastack, cell_type_table):
        client = make_client(datastack, c.server_address)

        if cell_type_table == "" or cell_type_table is None:
            return [{"name": i, "id": i} for i in c.table_columns], [], {}

        if c.debug:
            print("cell_type_table", cell_type_table, "client", client.datastack_name)
        _, val_cols = get_table_info(
            cell_type_table, client, allow_types=ALLOW_COLUMN_TYPES_DISCRETE
        )

        table_cons = c.table_columns + val_cols
        table_values = client.materialize.get_unique_string_values(cell_type_table)
        return (
            [{"name": i, "id": i} for i in table_cons],
            [{"label": k, "value": k} for k in val_cols],
            table_values,
        )

    @app.callback(
        OutputCellTypeValue,
        InputMaterializationVersion,
    )
    def clear_cell_type_dropdown(mat_version):
        return ""

    @app.callback(
        Output("plot-color-value", "options"),
        Output("plot-color-value", "value"),
        Input("group-by", "options"),
        Input("plot-color-value", "value"),
    )
    def update_plot_options(new_options, old_value):
        DEFAULT_VALUE = "cell_type"
        option_labels = [v["label"] for v in new_options]
        if old_value in option_labels:
            new_value = old_value
        elif DEFAULT_VALUE in new_options:
            new_value = DEFAULT_VALUE
        else:
            new_value = ""
        return new_options, new_value

    @app.callback(
        OutputDatastack,
        InputDatastack,
    )
    def define_datastack(datastack):
        if datastack is None:
            datastack = ""

        if len(datastack) == 0:
            return c.default_datastack
        else:
            return datastack

    @app.callback(
        OutputCellTypeMenuOptions,
        InputDatastack,
        InputMaterializationVersion,
    )
    def set_cell_type_dropdown(datastack, mat_version):
        if c.debug:
            print("Triggered cell type dropdown options")
        type_tables = get_type_tables(datastack, c, mat_version)
        return type_tables

    @app.callback(
        Output("message-text", "children"),
        Output("message-text", "color"),
        Output("main-loading-placeholder", "children"),
        Output("target-table-json", "data"),
        Output("source-table-json", "data"),
        Output("output-tab", "label"),
        Output("input-tab", "label"),
        Output("reset-selection", "n_clicks"),
        Output("client-info-json", "data"),
        Output("violin-plot", "children"),
        Output("synapse-table-resolution-json", "data"),
        Input("submit-button", "n_clicks"),
        InputDatastack,
        StateRootID,
        StateAnnoType,
        StateCellTypeTable,
        StateMaterializationVersion,
    )
    def update_data(_1, datastack_name, anno_id, id_type, ct_table_value, mat_version):
        if logger is not None:
            t0 = time.time()
        if c.debug:
            print("Mat version:", mat_version)

        if mat_version == "live" or "":
            version = None
        else:
            version = mat_version

        try:
            client = make_client(
                datastack_name, c.server_address, materialize_version=version
            )
            if version is None:
                version = client.materialize.version
            info_cache = client.info.info_cache[datastack_name]
            info_cache["global_server"] = client.server_address

        except Exception as e:
            print(traceback.format_exc())
            return (
                html.Div(str(e)),
                "danger",
                "",
                [],
                [],
                "Output",
                "Input",
                1,
                EMPTY_INFO_CACHE,
                make_violin_plot(None),
                None,
            )

        if not ct_table_value:
            ct_table_value = None
        info_cache["cell_type_column"] = ct_table_value

        if mat_version == "live":
            live_query = True
        else:
            live_query = False

        if live_query:
            timestamp = datetime.datetime.now(tz=pytz.UTC)
            timestamp_ngl = None
            info_cache["ngl_timestamp"] = None
        else:
            timestamp = client.materialize.get_timestamp(version=version)
            timestamp_ngl = timestamp
            info_cache["ngl_timestamp"] = timestamp.timestamp()

        if anno_id is None or len(anno_id) == 0:
            return (
                html.Div("Please select a cell id and press Submit"),
                "info",
                "",
                [],
                [],
                "Output",
                "Input",
                1,
                info_cache,
                make_violin_plot(None),
                None,
            )
        else:
            if id_type == "root_id":
                object_id = int(anno_id)
                object_id_type = "root"
            elif id_type == "nucleus_id":
                object_id = int(anno_id)
                object_id_type = "nucleus"
            else:
                raise ValueError('id_type must be either "root_id" or "nucleus_id"')

        try:
            nrn_data = NeuronData(
                object_id=object_id,
                client=client,
                config=c,
                value_table=ct_table_value,
                timestamp=timestamp,
                id_type=object_id_type,
                is_live=live_query,
                n_threads=2,
            )
            if c.debug:
                print(
                    f"\nMade NeuronData object with nuc table: {nrn_data._soma_table}\n"
                )

            root_id = nrn_data.root_id
            info_cache["root_id"] = str(root_id)

            if c.debug:
                print(f"\n Starting partners out")
            pre_targ_df = nrn_data.partners_out_plus()
            pre_targ_df = stringify_root_ids(
                pre_targ_df, stringify_cols=[c.root_id_col]
            )

            if c.debug:
                print(f"\n Starting partners in")
            post_targ_df = nrn_data.partners_in_plus()
            post_targ_df = stringify_root_ids(
                post_targ_df, stringify_cols=[c.root_id_col]
            )

            n_syn_pre = pre_targ_df[c.num_syn_col].sum()
            n_syn_post = post_targ_df[c.num_syn_col].sum()

            for col in nrn_data.config.syn_pt_position_split:
                stringify_list(col, pre_targ_df)
                stringify_list(col, post_targ_df)

            if logger is not None:
                logger.info(
                    f"Data update for {root_id} | time:{time.time() - t0:.2f} s, syn_in: {len(pre_targ_df)} , syn_out: {len(post_targ_df)}"
                )
            if nrn_data.nucleus_id is not None and nrn_data.soma_table is not None:
                if np.issubdtype(type(nrn_data.nucleus_id), np.integer):
                    nuc_id_text = f"  (nucleus id: {nrn_data.nucleus_id})"
                else:
                    nuc_id_text = f" (Multiple nucleus ids in segment: {', '.join([str(x) for x in nrn_data.nucleus_id])})"
            else:
                nuc_id_text = ""
            if ct_table_value:
                ct_text = f"table {ct_table_value}"
            else:
                ct_text = "no cell type table"

            if nrn_data.old_root_id is not None:
                change_root_id_text = f" Warning: {nrn_data.old_root_id} is not valid at timestamp queried! Showing data for the most overlapping valid root id. — "
                output_status = "warning"
            else:
                change_root_id_text = ""
                output_status = "success"

            if live_query:
                message_text = f"{change_root_id_text}Current connectivity for root id {root_id}{nuc_id_text} and {ct_text}."
            else:
                message_text = f"{change_root_id_text}Connectivity for root id {root_id}{nuc_id_text} and {ct_text} materialized on {timestamp_ngl:%m/%d/%Y} (v{client.materialize.version})"

            if c.show_depth_plots:
                vplot = make_violin_plot(nrn_data, None)
            else:
                vplot = make_violin_plot(None)
            syn_res = nrn_data.synapse_data_resolution
            del nrn_data
            del client

            return (
                html.Div(message_text),
                output_status,
                "",
                pre_targ_df.to_dict("records"),
                post_targ_df.to_dict("records"),
                f"Output (n = {n_syn_pre})",
                f"Input (n = {n_syn_post})",
                1,
                info_cache,
                vplot,
                syn_res,
            )
        except Exception as e:
            if c.debug:
                print(f"Failed on datastack {datastack_name}!")
                print(
                    "\n",
                    info_cache,
                    "\n",
                )
                print(traceback.format_exc())
            return (
                html.Div(str(e)),
                "danger",
                "",
                [],
                [],
                "Output",
                "Input",
                1,
                EMPTY_INFO_CACHE,
                make_violin_plot(None),
                None,
            )

    @app.callback(
        Output("scatter-plot", "children"),
        Output("bar-plot", "children"),
        Input("target-table-json", "data"),
        Input("plot-color-value", "value"),
        Input("client-info-json", "data"),
        Input("unique-table-values", "data"),
    )
    def update_scatter_bar_plots(rows, color_column, info_cache, table_values):
        return make_ct_plots(
            rows, c, aligned_volume(info_cache), color_column, table_values
        )

    @app.callback(
        Output("data-table", "data"),
        Input("connectivity-tab", "value"),
        Input("target-table-json", "data"),
        Input("source-table-json", "data"),
    )
    def update_table(
        tab_value,
        pre_data,
        post_data,
    ):
        if tab_value == "tab-pre":
            return pre_data
        elif tab_value == "tab-post":
            return post_data
        else:
            return []

    @app.callback(
        Output("ngl-link", "href"),
        Output("ngl-link", "children"),
        Output("ngl-link", "disabled"),
        Output("link-loading", "children"),
        Input("connectivity-tab", "value"),
        Input("data-table", "derived_virtual_data"),
        Input("data-table", "derived_virtual_selected_rows"),
        Input("client-info-json", "data"),
        Input("synapse-table-resolution-json", "data"),
        Input("ngl-target-site", "value"),
        InputDatastack,
    )
    def update_link(
        tab_value,
        rows,
        selected_rows,
        info_cache,
        synapse_data_resolution,
        target_site,
        datastack_name,
    ):
        if c.debug:
            print(f"Target site: {target_site}")
        large_state_text = (
            "Table Too Large - Please Filter or Use Whole Cell Neuroglancer Links"
        )

        def small_state_text(n):
            return f"Neuroglancer: ({n} partners)"

        if info_cache is None:
            client = make_client(datastack_name, c.server_address)
            info_cache = client.info.info_cache[datastack_name]

        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )
        if c.debug:
            print("generating link")
            print(info_cache)
        if rows is None or len(rows) == 0:
            rows = {}
            sb = generate_statebuilder(info_cache, c)
            return (
                sb.render_state(None, return_as="url"),
                small_state_text(0),
                False,
                "",
            )
        else:
            syn_df = rehydrate_dataframe(rows, c.syn_pt_position_split)

            if len(selected_rows) == 0:
                if tab_value == "tab-pre":
                    sb = generate_statebuilder_pre(
                        info_cache, c, data_resolution=synapse_data_resolution
                    )
                elif tab_value == "tab-post":
                    sb = generate_statebuilder_post(
                        info_cache, c, data_resolution=synapse_data_resolution
                    )
                else:
                    raise ValueError('tab must be "tab-pre" or "tab-post"')
                url = sb.render_state(
                    syn_df.sort_values(by=c.num_syn_col, ascending=False),
                    return_as="url",
                )
                small_out_text = small_state_text(len(syn_df))

            else:
                if tab_value == "tab-pre":
                    anno_layer = "Output Synapses"
                elif tab_value == "tab-post":
                    anno_layer = "Input Synapses"
                sb = generate_statebuider_syn_grouped(
                    info_cache,
                    anno_layer,
                    c,
                    preselect=len(selected_rows) == 1,
                    data_resolution=synapse_data_resolution,
                )
                url = sb.render_state(
                    syn_df.iloc[selected_rows].sort_values(
                        by=c.num_syn_col, ascending=False
                    ),
                    return_as="url",
                )
                small_out_text = small_state_text(len(selected_rows))

        if len(url) > MAX_URL_LENGTH:
            return "", large_state_text, True, ""
        else:
            return url, small_out_text, False, ""

    @app.callback(
        Output("all-input-link", "children"),
        Output("all-input-link-button", "children"),
        Output("all-input-link-button", "disabled"),
        Input("all-input-link-button", "n_clicks"),
        Input("all-input-link-button", "children"),
        Input("submit-button", "n_clicks"),
        Input("source-table-json", "data"),
        Input("client-info-json", "data"),
        InputDatastack,
        Input("synapse-table-resolution-json", "data"),
        Input("ngl-target-site", "value"),
        prevent_initial_call=True,
    )
    def generate_all_input_link(
        _1,
        _2,
        curr,
        rows,
        info_cache,
        datastack,
        data_resolution,
        target_site,
    ):
        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if not allowed_action_trigger(callback_context, ["all-input-link-button"]):
            return "  ", "Generate Link", False
        return (
            generic_syn_link_generation(
                partial(
                    generate_statebuilder_post,
                    config=c,
                    data_resolution=data_resolution,
                ),
                rows,
                info_cache,
                datastack,
                c,
                "Neuroglancer Link",
                "Inputs",
            ),
            "Link Generated",
            True,
        )

    @app.callback(
        Output("cell-typed-input-link", "children"),
        Output("cell-typed-input-link-button", "children"),
        Output("cell-typed-input-link-button", "disabled"),
        Input("cell-typed-input-link-button", "n_clicks"),
        Input("submit-button", "n_clicks"),
        Input("source-table-json", "data"),
        Input("client-info-json", "data"),
        InputDatastack,
        Input("synapse-table-resolution-json", "data"),
        Input("group-by", "value"),
        Input("no-type-annotation", "value"),
        Input("ngl-target-site", "value"),
        prevent_initial_call=True,
    )
    def generate_cell_typed_input_link(
        _1,
        _2,
        rows,
        info_cache,
        datastack,
        data_resolution,
        value_column,
        include_no_type,
        target_site,
    ):
        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if value_column is None or value_column == "":
            return "  ", "No Annotation Column Set", True
        if not allowed_action_trigger(
            callback_context, ["cell-typed-input-link-button"]
        ):
            return "  ", "Generate Link", False

        include_no_type = 1 in include_no_type

        sb, dfs = generate_statebuilder_syn_cell_types(
            info_cache,
            rows,
            c,
            cell_type_column=value_column,
            multipoint=True,
            fill_null="NoType",
            data_resolution=data_resolution,
            include_no_type=include_no_type,
        )
        try:
            url = make_url_robust(dfs, sb, datastack, c)
        except Exception as e:
            return html.Div(str(e))
        return (
            html.A(
                "Grouped Input Link",
                href=url,
                target="_blank",
                style={"font-size": "20px"},
            ),
            "Link Generated",
            True,
        )

    @app.callback(
        Output("all-output-link", "children"),
        Output("all-output-link-button", "children"),
        Output("all-output-link-button", "disabled"),
        Input("all-output-link-button", "n_clicks"),
        Input("submit-button", "n_clicks"),
        Input("target-table-json", "data"),
        Input("client-info-json", "data"),
        InputDatastack,
        Input("synapse-table-resolution-json", "data"),
        Input("ngl-target-site", "value"),
        prevent_initial_call=True,
    )
    def generate_all_output_link(
        _1, _2, rows, info_cache, datastack, data_resolution, target_site
    ):
        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if not allowed_action_trigger(callback_context, ["all-output-link-button"]):
            return "", "Generate Link", False
        return (
            generic_syn_link_generation(
                partial(
                    generate_statebuilder_pre, config=c, data_resolution=data_resolution
                ),
                rows,
                info_cache,
                datastack,
                c,
                "All Output Link",
                "Outputs",
            ),
            "Link Generated",
            True,
        )

    @app.callback(
        Output("cell-typed-output-link", "children"),
        Output("cell-typed-output-link-button", "children"),
        Output("cell-typed-output-link-button", "disabled"),
        Input("cell-typed-output-link-button", "n_clicks"),
        Input("submit-button", "n_clicks"),
        Input("target-table-json", "data"),
        Input("client-info-json", "data"),
        InputDatastack,
        Input("synapse-table-resolution-json", "data"),
        Input("group-by", "value"),
        Input("no-type-annotation", "value"),
        Input("ngl-target-site", "value"),
        prevent_initial_call=True,
    )
    def generate_cell_typed_output_link(
        _1,
        _2,
        rows,
        info_cache,
        datastack,
        data_resolution,
        value_column,
        include_no_type,
        target_site,
    ):
        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if value_column is None or value_column == "":
            return "  ", "No Annotation Column Set", True

        if not allowed_action_trigger(
            callback_context, ["cell-typed-output-link-button"]
        ):
            return "  ", "Generate Link", False

        include_no_type = 1 in include_no_type

        sb, df_dict = generate_statebuilder_syn_cell_types(
            info_cache,
            rows,
            c,
            cell_type_column=value_column,
            multipoint=True,
            fill_null="NoType",
            data_resolution=data_resolution,
            include_no_type=include_no_type,
        )
        try:
            url = make_url_robust(df_dict, sb, datastack, c)
        except Exception as e:
            return html.Div(str(e))
        return (
            html.A(
                "Cell Typed Output Link",
                href=url,
                target="_blank",
                style={"font-size": "20px"},
            ),
            "Link Generated",
            True,
        )

    @app.callback(
        Output("collapse-card", "is_open"),
        Input("collapse-button", "n_clicks"),
        State("collapse-card", "is_open"),
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("plot-collapse", "is_open"),
        Input("plot-collapse-button", "n_clicks"),
        State("plot-collapse", "is_open"),
    )
    def toggle_plot_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    pass
