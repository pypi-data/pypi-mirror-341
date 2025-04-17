import os
from typing import Any, Dict, Iterable, List, Optional

import click

from tinybird.tb.client import TinyB
from tinybird.tb.config import get_display_cloud_host
from tinybird.tb.modules.cli import CLIConfig, cli
from tinybird.tb.modules.common import coro, format_robust_table
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_LOCAL_ADDRESS, get_tinybird_local_config
from tinybird.tb.modules.project import Project


@cli.command(name="info")
@click.pass_context
@coro
async def info(ctx: click.Context) -> None:
    """Get information about the project that is currently being used"""
    ctx_config = ctx.ensure_object(dict)["config"]
    project: Project = ctx.ensure_object(dict)["project"]
    click.echo(FeedbackManager.highlight(message="» Tinybird Cloud:"))
    await get_cloud_info(ctx_config)
    click.echo(FeedbackManager.highlight(message="\n» Tinybird Local:"))
    await get_local_info(ctx_config)
    click.echo(FeedbackManager.highlight(message="\n» Project:"))
    await get_project_info(project.folder)


async def get_cloud_info(ctx_config: Dict[str, Any]) -> None:
    config = CLIConfig.get_project_config()

    try:
        client = config.get_client()
        token = config.get_token() or "No workspace token found"
        api_host = config.get("host") or "No API host found"
        ui_host = get_display_cloud_host(api_host)
        user_email = config.get("user_email") or "No user email found"
        user_token = config.get_user_token() or "No user token found"
        await get_env_info(client, ctx_config, user_email, token, user_token, api_host, ui_host)
    except Exception:
        click.echo(
            FeedbackManager.warning(
                message="\n⚠  Could not retrieve Tinybird Cloud info. Please run `tb login` first or check that you are located in the correct directory."
            )
        )


async def get_local_info(config: Dict[str, Any]) -> None:
    try:
        local_config = await get_tinybird_local_config(config, test=False, silent=False)
        local_client = local_config.get_client(host=TB_LOCAL_ADDRESS, staging=False)
        user_email = local_config.get_user_email() or "No user email found"
        token = local_config.get_token() or "No token found"
        user_token = local_config.get_user_token() or "No user token found"
        api_host = TB_LOCAL_ADDRESS
        ui_host = get_display_cloud_host(api_host)
        await get_env_info(local_client, config, user_email, token, user_token, api_host, ui_host)
    except Exception:
        click.echo(
            FeedbackManager.warning(
                message="\n⚠  Could not retrieve Tinybird Local info. Please run `tb local start` first."
            )
        )
        return


async def get_env_info(
    client: TinyB, config: Dict[str, Any], user_email: str, token: str, user_token: str, api_host: str, ui_host: str
) -> None:
    user_workspaces = await client.user_workspaces(version="v1")
    current_workspace = await client.workspace_info(version="v1")

    def _get_current_workspace(user_workspaces: Dict[str, Any], current_workspace_id: str) -> Optional[Dict[str, Any]]:
        def get_workspace_by_name(workspaces: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
            return next((ws for ws in workspaces if ws["name"] == name), None)

        workspaces: Optional[List[Dict[str, Any]]] = user_workspaces.get("workspaces")
        if not workspaces:
            return None

        current: Optional[Dict[str, Any]] = get_workspace_by_name(workspaces, current_workspace_id)
        return current

    current_main_workspace = _get_current_workspace(user_workspaces, config.get("name") or current_workspace["name"])

    assert isinstance(current_main_workspace, dict)

    columns = ["user", "workspace_name", "workspace_id", "token", "user_token", "api", "ui"]
    if current_main_workspace["name"]:
        ui_host += f"/{current_main_workspace['name']}"
    table = [
        (user_email, current_main_workspace["name"], current_main_workspace["id"], token, user_token, api_host, ui_host)
    ]

    click.echo(format_robust_table(table, column_names=columns))


async def get_project_info(project_path: Optional[str] = None) -> None:
    config = CLIConfig.get_project_config()
    tinyb_path = config.get_tinyb_file()
    current_path = os.getcwd()
    project_path = current_path
    if tinyb_path:
        tinyb_dir = os.path.dirname(tinyb_path)
        project_path = os.path.join(tinyb_dir, project_path)
    else:
        tinyb_path = "Not found"

    columns = ["current", ".tinyb", "project"]
    table: Iterable[Any] = [(current_path, tinyb_path, project_path)]
    click.echo(format_robust_table(table, column_names=columns))
