from dependency_injector import containers, providers

from aether.application.use_cases.process_chat import ProcessChatUseCase
from aether.config.settings import Settings, settings
from aether.infrastructure.llm.ollama_adapter import OllamaLLMAdapter


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "aether.presentation.api.routes",
            "aether.presentation.ws.session",
        ]
    )

    config = providers.Singleton(lambda: settings)

    llm_adapter = providers.Singleton(
        OllamaLLMAdapter,
        settings=config,
    )

    process_chat_use_case_factory = providers.Factory(
        ProcessChatUseCase,
        llm=llm_adapter,
    )


def create_container() -> Container:
    container = Container()
    container.init_resources()
    return container
