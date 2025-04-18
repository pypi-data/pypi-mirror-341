"""
Web application for the Ultimate RVC project.

Each tab of the application is defined in its own module in the
`web/tabs` directory. Components that are accessed across multiple
tabs are passed as arguments to the render functions in the respective
modules.
"""

from __future__ import annotations

from typing import Annotated

import os

import gradio as gr

import typer

from ultimate_rvc.common import AUDIO_DIR, MODELS_DIR, TEMP_DIR
from ultimate_rvc.core.generate.song_cover import get_named_song_dirs
from ultimate_rvc.core.generate.speech import get_edge_tts_voice_names
from ultimate_rvc.core.manage.audio import (
    get_audio_datasets,
    get_named_audio_datasets,
    get_saved_output_audio,
    get_saved_speech_audio,
)
from ultimate_rvc.core.manage.models import (
    get_custom_embedder_model_names,
    get_custom_pretrained_model_names,
    get_training_model_names,
    get_voice_model_names,
)
from ultimate_rvc.web.common import update_total_config
from ultimate_rvc.web.config.main import TotalConfig
from ultimate_rvc.web.tabs.generate.song_cover.multi_step_generation import (
    render as render_song_cover_multi_step_tab,
)
from ultimate_rvc.web.tabs.generate.song_cover.one_click_generation import (
    render as render_song_cover_one_click_tab,
)
from ultimate_rvc.web.tabs.generate.speech.multi_step_generation import (
    render as render_speech_multi_step_tab,
)
from ultimate_rvc.web.tabs.generate.speech.one_click_generation import (
    render as render_speech_one_click_tab,
)
from ultimate_rvc.web.tabs.manage.audio import render as render_manage_audio_tab
from ultimate_rvc.web.tabs.manage.models import render as render_manage_models_tab
from ultimate_rvc.web.tabs.manage.settings import render as render_settings_tab
from ultimate_rvc.web.tabs.train.multi_step_generation import (
    render as render_train_multi_step_tab,
)

total_config = TotalConfig()
config_name = os.environ.get("URVC_CONFIG")
if config_name:
    update_total_config(config_name, total_config)
cookiefile = os.environ.get("YT_COOKIEFILE")


def render_app() -> gr.Blocks:
    """
    Render the Ultimate RVC web application.

    Returns
    -------
    gr.Blocks
        The rendered web application.

    """
    css = """
    h1 { text-align: center; margin-top: 20px; margin-bottom: 20px; }
    """
    cache_delete_frequency = 86400  # every 24 hours check for files to delete
    cache_delete_cutoff = 86400  # and delete files older than 24 hours

    with gr.Blocks(
        title="Ultimate RVC",
        css=css,
        delete_cache=(cache_delete_frequency, cache_delete_cutoff),
    ) as app:
        gr.HTML("<h1>Ultimate RVC 🧡</h1>")

        voice_model_names = get_voice_model_names()
        for component_config in [
            total_config.song.one_click.voice_model,
            total_config.song.multi_step.voice_model,
            total_config.speech.one_click.voice_model,
            total_config.speech.multi_step.voice_model,
        ]:
            component_config.instantiate(choices=voice_model_names)
        named_song_dirs = get_named_song_dirs()
        for component_config in [
            total_config.song.multi_step.song_dirs.separate_audio,
            total_config.song.multi_step.song_dirs.convert_vocals,
            total_config.song.multi_step.song_dirs.postprocess_vocals,
            total_config.song.multi_step.song_dirs.pitch_shift_background,
            total_config.song.multi_step.song_dirs.mix,
        ]:
            component_config.instantiate(choices=named_song_dirs)
        for component_config in [
            total_config.song.one_click.cached_song,
            total_config.song.one_click.custom_embedder_model,
            total_config.song.multi_step.cached_song,
            total_config.song.multi_step.custom_embedder_model,
            total_config.speech.one_click.edge_tts_voice,
            total_config.speech.one_click.custom_embedder_model,
            total_config.speech.multi_step.edge_tts_voice,
            total_config.speech.multi_step.custom_embedder_model,
            total_config.training.multi_step.dataset,
            total_config.training.multi_step.preprocess_model,
            total_config.training.multi_step.extract_model,
            total_config.training.multi_step.train_model,
            total_config.training.multi_step.custom_embedder_model,
            total_config.training.multi_step.custom_pretrained_model,
            total_config.management.audio.intermediate,
            total_config.management.audio.speech,
            total_config.management.audio.output,
            total_config.management.audio.dataset,
            total_config.management.model.voices,
            total_config.management.model.embedders,
            total_config.management.model.pretraineds,
            total_config.management.model.traineds,
        ]:
            component_config.instantiate(use_gradio_default=True)
        # main tab
        with gr.Tab("Generate song covers"):
            render_song_cover_one_click_tab(total_config, cookiefile)
            render_song_cover_multi_step_tab(total_config, cookiefile)
        with gr.Tab("Generate speech"):
            render_speech_one_click_tab(total_config)
            render_speech_multi_step_tab(total_config)
        with gr.Tab("Train voice models"):
            render_train_multi_step_tab(total_config)
        with gr.Tab("Manage models"):
            render_manage_models_tab(total_config)
        with gr.Tab("Manage audio"):
            render_manage_audio_tab(total_config)
        with gr.Tab("Settings"):
            render_settings_tab(total_config)

        app.load(
            _init_app,
            outputs=[
                total_config.speech.one_click.edge_tts_voice.instance,
                total_config.speech.multi_step.edge_tts_voice.instance,
                total_config.song.one_click.voice_model.instance,
                total_config.song.multi_step.voice_model.instance,
                total_config.speech.one_click.voice_model.instance,
                total_config.speech.multi_step.voice_model.instance,
                total_config.management.model.voices.instance,
                total_config.song.one_click.custom_embedder_model.instance,
                total_config.song.multi_step.custom_embedder_model.instance,
                total_config.speech.one_click.custom_embedder_model.instance,
                total_config.speech.multi_step.custom_embedder_model.instance,
                total_config.training.multi_step.custom_embedder_model.instance,
                total_config.management.model.embedders.instance,
                total_config.training.multi_step.custom_pretrained_model.instance,
                total_config.management.model.pretraineds.instance,
                total_config.training.multi_step.preprocess_model.instance,
                total_config.training.multi_step.extract_model.instance,
                total_config.training.multi_step.train_model.instance,
                total_config.management.model.traineds.instance,
                total_config.song.one_click.cached_song.instance,
                total_config.song.multi_step.cached_song.instance,
                total_config.management.audio.intermediate.instance,
                total_config.song.multi_step.song_dirs.separate_audio.instance,
                total_config.song.multi_step.song_dirs.convert_vocals.instance,
                total_config.song.multi_step.song_dirs.postprocess_vocals.instance,
                total_config.song.multi_step.song_dirs.pitch_shift_background.instance,
                total_config.song.multi_step.song_dirs.mix.instance,
                total_config.training.multi_step.dataset.instance,
                total_config.management.audio.speech.instance,
                total_config.management.audio.output.instance,
                total_config.management.audio.dataset.instance,
            ],
            show_progress="hidden",
        )
    return app


def _init_app() -> list[gr.Dropdown]:
    """
    Initialize the Ultimate RVC web application by updating the choices
    of all dropdown components.

    Returns
    -------
    tuple[gr.Dropdown, ...]
        Updated dropdowns for selecting models and audio files.

    """
    # Initialize model dropdowns
    tts_voice_names = get_edge_tts_voice_names()
    christopher_voice = "en-US-ChristopherNeural"
    default_voice_name = (
        christopher_voice
        if christopher_voice in tts_voice_names
        else next(iter(tts_voice_names), None)
    )
    edge_tts_voice_1click, edge_tts_voice_multi = [
        gr.Dropdown(choices=tts_voice_names, value=default_voice_name) for _ in range(2)
    ]
    voice_model_names = get_voice_model_names()
    voice_models = [
        gr.Dropdown(
            choices=voice_model_names,
            value=next(iter(voice_model_names), None),
        )
        for _ in range(4)
    ]
    voice_model_delete = gr.Dropdown(choices=voice_model_names)
    custom_embedder_models = [
        gr.Dropdown(choices=get_custom_embedder_model_names()) for _ in range(6)
    ]

    custom_pretrained_models = [
        gr.Dropdown(choices=get_custom_pretrained_model_names()) for _ in range(2)
    ]
    training_models = [
        gr.Dropdown(choices=get_training_model_names()) for _ in range(4)
    ]

    # Initialize audio dropdowns
    named_song_dirs = get_named_song_dirs()
    cached_songs = [gr.Dropdown(choices=named_song_dirs) for _ in range(3)]
    song_dirs = [
        gr.Dropdown(
            choices=named_song_dirs,
            value=None if not named_song_dirs else named_song_dirs[0][1],
        )
        for _ in range(5)
    ]
    dataset = gr.Dropdown(choices=get_audio_datasets())
    speech_delete = gr.Dropdown(choices=get_saved_speech_audio())
    output_delete = gr.Dropdown(choices=get_saved_output_audio())
    dataset_delete = gr.Dropdown(choices=get_named_audio_datasets())
    return [
        edge_tts_voice_1click,
        edge_tts_voice_multi,
        *voice_models,
        voice_model_delete,
        *custom_embedder_models,
        *custom_pretrained_models,
        *training_models,
        *cached_songs,
        *song_dirs,
        dataset,
        speech_delete,
        output_delete,
        dataset_delete,
    ]


app = render_app()
app_wrapper = typer.Typer()


@app_wrapper.command()
def start_app(
    share: Annotated[
        bool,
        typer.Option("--share", "-s", help="Enable sharing"),
    ] = False,
    listen: Annotated[
        bool,
        typer.Option(
            "--listen",
            "-l",
            help="Make the web application reachable from your local network.",
        ),
    ] = False,
    listen_host: Annotated[
        str | None,
        typer.Option(
            "--listen-host",
            "-h",
            help="The hostname that the server will use.",
        ),
    ] = None,
    listen_port: Annotated[
        int | None,
        typer.Option(
            "--listen-port",
            "-p",
            help="The listening port that the server will use.",
        ),
    ] = None,
    ssr_mode: Annotated[
        bool,
        typer.Option(
            "--ssr-mode",
            help="Enable server-side rendering mode.",
        ),
    ] = False,
) -> None:
    """Run the Ultimate RVC web application."""
    os.environ["GRADIO_TEMP_DIR"] = str(TEMP_DIR)
    gr.set_static_paths([MODELS_DIR, AUDIO_DIR])
    app.queue()
    app.launch(
        share=share,
        server_name=(None if not listen else (listen_host or "0.0.0.0")),  # noqa: S104
        server_port=listen_port,
        ssr_mode=ssr_mode,
    )


if __name__ == "__main__":
    app_wrapper()
