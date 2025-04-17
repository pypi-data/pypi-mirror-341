from dash import html
import numpy as np
import pytz
from ..common.neuron_data_base import NeuronData
from dash.dependencies import Input, Output, State
from dash import callback_context

from ..common.link_utilities import (
    generate_statebuider_syn_grouped,
    generate_statebuilder,
    generate_statebuilder_pre,
    generate_statebuilder_post,
    EMPTY_INFO_CACHE,
    MAX_URL_LENGTH,
    make_url_robust,
    get_viewer_site_from_target,
)
from ..common.dataframe_utilities import (
    stringify_root_ids,
    stringify_list,
    repopulate_list,
)
from ..common.dash_url_helper import _COMPONENT_ID_TYPE
from ..common.lookup_utilities import make_client, get_version_options
from .config import ConnectivityConfig

import datetime
import pandas as pd

try:
    from loguru import logger
    import time
except:
    logger = None


InputDatastack = Input({"id_inner": "datastack", "type": _COMPONENT_ID_TYPE}, "value")
OutputDatastack = Output({"id_inner": "datastack", "type": _COMPONENT_ID_TYPE}, "value")
StateAnnoID = State({"id_inner": "anno-id", "type": _COMPONENT_ID_TYPE}, "value")
StateAnnoType = State({"id_inner": "cell-id-type", "type": _COMPONENT_ID_TYPE}, "value")


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


def register_callbacks(app, config):
    c = ConnectivityConfig(config)

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
            f"Connectivity Info — {datastack}",
            className="bg-primary text-white p-2 mb-2 text-center",
        )

    @app.callback(
        Output("data-table", "columns"),
        InputDatastack,
    )
    def define_table_columns(_):
        return [{"name": i, "id": i} for i in c.table_columns]

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
        Output("target-table-json", "data"),
        Output("source-table-json", "data"),
        Output("output-tab", "label"),
        Output("input-tab", "label"),
        Output("reset-selection", "n_clicks"),
        Output("client-info-json", "data"),
        Output("loading-spinner", "children"),
        Output("message-text", "children"),
        Output("message-text", "color"),
        Output("synapse-table-resolution-json", "data"),
        Input("submit-button", "n_clicks"),
        InputDatastack,
        StateAnnoID,
        StateAnnoType,
        StateMaterializationVersion,
    )
    def update_data(_, datastack_name, anno_id, id_type, mat_version):
        if logger is not None:
            t0 = time.time()

        if mat_version == "live" or mat_version == "":
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
            return (
                [],
                [],
                "Output",
                "Input",
                1,
                EMPTY_INFO_CACHE,
                "",
                str(e),
                "danger",
                None,
            )

        if len(anno_id) == 0:
            return (
                [],
                [],
                "Output",
                "Input",
                1,
                info_cache,
                "",
                "No annotation id selected",
                "info",
                None,
            )

        if len(anno_id) == 0:
            anno_id = None
            id_type = "anno_id"

        live_query = mat_version == "live"

        if live_query:
            timestamp = datetime.datetime.now(tz=pytz.UTC)
            timestamp_ngl = None
            info_cache["ngl_timestamp"] = None
        else:
            timestamp = client.materialize.get_timestamp()
            timestamp_ngl = client.materialize.get_timestamp()
            info_cache["ngl_timestamp"] = timestamp_ngl.timestamp()

        if anno_id is None:
            root_id = None
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
                timestamp=timestamp,
                id_type=object_id_type,
                n_threads=1,
                is_live=live_query,
            )

            root_id = nrn_data.root_id

            pre_targ_df = nrn_data.partners_out()
            pre_targ_df = stringify_root_ids(
                pre_targ_df, stringify_cols=[c.root_id_col]
            )

            post_targ_df = nrn_data.partners_in()
            post_targ_df = stringify_root_ids(
                post_targ_df, stringify_cols=[c.root_id_col]
            )
            for col in nrn_data.config.syn_pt_position_split:
                stringify_list(col, pre_targ_df)
                stringify_list(col, post_targ_df)

            n_syn_pre = pre_targ_df[c.num_syn_col].sum()
            n_syn_post = post_targ_df[c.num_syn_col].sum()

            info_cache["root_id"] = str(root_id)

        except Exception as e:
            return (
                [],
                [],
                "Output",
                "Input",
                1,
                info_cache,
                "",
                str(e),
                "danger",
                None,
            )

        if logger is not None:
            logger.info(
                f"Data update for {root_id} | time:{time.time() - t0:.2f} s, syn_in: {n_syn_post} , syn_out: {n_syn_pre}"
            )

        if nrn_data.old_root_id is not None:
            change_root_id_text = f" Warning: {nrn_data.old_root_id} is not valid at timestamp queried! Showing data for the most overlapping valid root id. —"
            output_status = "warning"
        else:
            change_root_id_text = ""
            output_status = "success"

        if nrn_data.nucleus_id is not None and nrn_data.soma_table is not None:
            if np.issubdtype(type(nrn_data.nucleus_id), np.integer):
                nuc_id_text = f"  (nucleus id: {nrn_data.nucleus_id})"
            else:
                nuc_id_text = f" (Multiple nucleus ids in segment: {', '.join([str(x) for x in nrn_data.nucleus_id])})"
        else:
            nuc_id_text = ""

        if live_query:
            output_message = f"{change_root_id_text}Current connectivity for root id {root_id}{nuc_id_text}."
        else:
            output_message = f"{change_root_id_text}Connectivity for root id {root_id}{nuc_id_text} materialized on {timestamp_ngl:%m/%d/%Y} (v{client.materialize.version})."

        return (
            pre_targ_df.to_dict("records"),
            post_targ_df.to_dict("records"),
            f"Output (n = {n_syn_pre})",
            f"Input (n = {n_syn_post})",
            1,
            info_cache,
            "",
            output_message,
            output_status,
            nrn_data.synapse_data_resolution,
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
        Output("ngl_link", "href"),
        Output("ngl_link", "children"),
        Output("ngl_link", "disabled"),
        Output("link-loading", "children"),
        Input("connectivity-tab", "value"),
        Input("data-table", "derived_virtual_data"),
        Input("data-table", "derived_virtual_selected_rows"),
        Input("client-info-json", "data"),
        Input("synapse-table-resolution-json", "data"),
        Input("ngl-target-site", "value"),
    )
    def update_link(
        tab_value,
        rows,
        selected_rows,
        info_cache,
        data_resolution,
        target_site,
    ):
        large_state_text = "State Too Large - Please Filter"

        def small_state_text(n):
            return f"Neuroglancer: ({n} partners)"

        if info_cache is None:
            return "", "No datastack set", True, ""

        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

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
            syn_df = pd.DataFrame(rows)
            for col in c.syn_pt_position_split:
                repopulate_list(col, syn_df)
            if len(selected_rows) == 0:
                if tab_value == "tab-pre":
                    sb = generate_statebuilder_pre(
                        info_cache, c, data_resolution=data_resolution
                    )
                elif tab_value == "tab-post":
                    sb = generate_statebuilder_post(
                        info_cache, c, data_resolution=data_resolution
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
                    data_resolution=data_resolution,
                )
                url = sb.render_state(syn_df.iloc[selected_rows], return_as="url")
                small_out_text = small_state_text(len(selected_rows))

        if len(url) > MAX_URL_LENGTH:
            return "", large_state_text, True, ""
        else:
            return url, small_out_text, False, ""

    @app.callback(
        Output("all-input-link", "children"),
        Input("all-input-link-button", "n_clicks"),
        Input("submit-button", "n_clicks"),
        Input("source-table-json", "data"),
        Input("client-info-json", "data"),
        InputDatastack,
        Input("synapse-table-resolution-json", "data"),
        Input("ngl-target-site", "value"),
        prevent_initial_call=True,
    )
    def generate_all_input_link(
        _1, _2, rows, info_cache, datastack, data_resolution, target_site
    ):
        ctx = callback_context
        if not ctx.triggered:
            return ""
        trigger_src = ctx.triggered[0]["prop_id"].split(".")[0]
        if (
            trigger_src == "submit-button"
            or trigger_src == "client-info-json"
            or trigger_src == "source-table-json"
        ):
            return ""

        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if rows is None or len(rows) == 0:
            return html.Div("No inputs to show")
        else:
            syn_df = pd.DataFrame(rows)
            for col in c.syn_pt_position_split:
                repopulate_list(col, syn_df)

            sb = generate_statebuilder_post(
                info_cache, c, data_resolution=data_resolution
            )
            try:
                url = make_url_robust(
                    syn_df.sort_values(by=c.num_syn_col, ascending=False),
                    sb,
                    datastack,
                    c,
                )
            except Exception as e:
                return html.Div(str(e))
        return html.A(
            "All Input Link", href=url, target="_blank", style={"font-size": "20px"}
        )

    @app.callback(
        Output("all-output-link", "children"),
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
        ctx = callback_context
        if not ctx.triggered:
            return ""
        trigger_src = ctx.triggered[0]["prop_id"].split(".")[0]
        if (
            trigger_src == "submit-button"
            or trigger_src == "client-info-json"
            or trigger_src == "target-table-json"
        ):
            return ""

        info_cache["target_site"] = target_site
        info_cache["viewer_site"] = get_viewer_site_from_target(
            info_cache.get("viewer_site"), target_site
        )

        if rows is None or len(rows) == 0:
            return html.Div("No outputs to show")
        else:
            syn_df = pd.DataFrame(rows)
            for col in c.syn_pt_position_split:
                repopulate_list(col, syn_df)
            sb = generate_statebuilder_pre(
                info_cache, c, data_resolution=data_resolution
            )

            try:
                url = make_url_robust(
                    syn_df.sort_values(by=c.num_syn_col, ascending=False),
                    sb,
                    datastack,
                    c,
                )
            except Exception as e:
                return html.Div(str(e))
        return html.A(
            "All Output Link", href=url, target="_blank", style={"font-size": "20px"}
        )

    pass
