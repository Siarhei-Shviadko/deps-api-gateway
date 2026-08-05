from cachetools import TTLCache
from dependency_injector import containers, providers

from deps_api_gateway.api.endpoints.v1.routers import (
    CorleoneRouter,
    DocumentRouter,
    DocumentTypeRouter,
    PreprocessRouter,
    PrototypeRouter,
    TemplateRouter,
    ValidationRouter,
)
from deps_api_gateway.application import (
    AgenticAIService,
    AIFusionService,
    BatchService,
    DocumentFieldAnalyticsService,
    DocumentService,
    DocumentTypeService,
    EventRelayService,
    ExtractionService,
    GroupService,
    IAgenticAIProxy,
    IAgenticAISSEProxy,
    IAIFusionProxy,
    IAMService,
    IBatchProxy,
    IClassificationProxy,
    ICloudNativeExtractionProxy,
    IDocumentFieldAnalyticsProxy,
    IDocumentProxy,
    IDocumentTypeProxy,
    IEnrichmentProxy,
    IEventRelayProxy,
    IExtraction,
    IGroupsProxy,
    IHighSparrowProxy,
    IIAMProxy,
    ILiteLLMProxy,
    IMetaAgentProxy,
    IOCRProxy,
    IOutputExportingProxy,
    IParsingProxy,
    ISemanticParsingProxy,
    ISplittingProxy,
    IStorageProxy,
    ITemplateProxy,
    IUnifierProxy,
    IWorkflowManagerProxy,
    LiteLLMService,
    MetaAgentService,
    OCRService,
    ParsingService,
    ParsingToolsService,
    ServiceDiscovery,
    SplittingService,
    StorageService,
    WorkflowService,
    legacy,
)
from deps_api_gateway.application.file.file_proxy import IFileProxy
from deps_api_gateway.application.file.service import FileService
from deps_api_gateway.infrastructure import (
    AgenticAIProxy,
    AgenticAISSEProxy,
    AIFusionProxy,
    AnalyticProxy,
    BatchProxy,
    ClassificationProxy,
    CloudNativeExtractionProxy,
    CorleoneProxy,
    DocumentProxy,
    DocumentTypeProxyOld,
    DocumentTypeProxyV1,
    DocumentTypeProxyV5,
    EnrichmentProxy,
    EventRelayProxy,
    ExtractionProxy,
    FileProxy,
    GroupsProxy,
    HighSparrowProxy,
    IAMProxy,
    IBackwardCompatiblePrototypeProxy,
    LiteLLMProxy,
    MetaAgentProxy,
    OCRProxy,
    OldDocumentProxy,
    OldEnrichmentProxy,
    OldExtractionProxy,
    OldGenericRestClient,
    OldOCRProxy,
    OldPrototypeProxy,
    OldUnifierProxy,
    OldWorkflowManagerProxy,
    OutputExportingProxy,
    ParsingProxy,
    PreprocessProxy,
    PrompterProxy,
    PrototypeProxy,
    SemanticParsingProxy,
    SplittingProxy,
    StorageProxy,
    TemplateProxy,
    UnifierProxy,
    WorkflowManagerProxy,
)


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    build_info: providers.Provider[dict] = providers.Dict(
        {
            "build_tag": config.info.tag,
            "build_date": config.info.date,
            "commit_hash": config.info.hash,
        },
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    corleone_generic_client: providers.Singleton[OldGenericRestClient] = providers.Singleton(
        OldGenericRestClient,
        base_url=config.corleone_url,
        verify_ssl=config.verify_ssl,
    )
    preprocess_generic_client: providers.Singleton[OldGenericRestClient] = providers.Singleton(
        OldGenericRestClient,
        base_url=config.preprocess_url,
        verify_ssl=config.verify_ssl,
    )
    validation_generic_client: providers.Singleton[OldGenericRestClient] = providers.Singleton(
        OldGenericRestClient,
        base_url=config.validation_url,
        verify_ssl=config.verify_ssl,
    )
    document_generic_client: providers.Singleton[OldGenericRestClient] = providers.Singleton(
        OldGenericRestClient,
        base_url=config.document_url,
        verify_ssl=config.verify_ssl,
    )
    template_generic_client: providers.Singleton[OldGenericRestClient] = providers.Singleton(
        OldGenericRestClient,
        base_url=config.template_url,
        verify_ssl=config.verify_ssl,
    )

    corleone_proxy: providers.Singleton[legacy.ICorleone] = providers.Singleton(
        CorleoneProxy,
        base_url=config.corleone_url,
        verify_ssl=config.verify_ssl,
    )
    preprocess_proxy: providers.Singleton[legacy.IPreprocess] = providers.Singleton(
        PreprocessProxy,
        base_url=config.preprocess_url,
    )
    old_document_proxy: providers.Singleton[legacy.IDocument] = providers.Singleton(
        OldDocumentProxy,
        base_url=config.document_url,
    )
    document_proxy: providers.Singleton[IDocumentProxy] = providers.Singleton(
        DocumentProxy,
        base_url=config.document_url,
    )
    document_type_proxy_old: providers.Singleton[legacy.IDocumentTypeOld] = providers.Singleton(
        DocumentTypeProxyOld,
        base_url=config.document_type_url,
        verify_ssl=config.verify_ssl,
    )
    document_type_proxy_v1: providers.Singleton[legacy.IDocumentType] = providers.Singleton(
        DocumentTypeProxyV1,
        base_url=config.document_type_url,
        verify_ssl=config.verify_ssl,
    )
    document_type_proxy_v5: providers.Singleton[IDocumentTypeProxy] = providers.Singleton(
        DocumentTypeProxyV5,
        base_url=config.document_type_url,
        verify_ssl=config.verify_ssl,
    )
    old_unifier_proxy: providers.Singleton[legacy.IUnifier] = providers.Singleton(
        OldUnifierProxy,
        base_url=config.unifier_url,
        verify_ssl=config.verify_ssl,
    )
    extraction_proxy: providers.Singleton[IExtraction] = providers.Singleton(
        ExtractionProxy,
        base_url=config.extraction_url,
        verify_ssl=config.verify_ssl,
    )
    old_extraction_proxy: providers.Singleton[legacy.IExtractionOld] = providers.Singleton(
        OldExtractionProxy,
        base_url=config.extraction_url,
        verify_ssl=config.verify_ssl,
    )
    workflow_manager_proxy: providers.Singleton[IWorkflowManagerProxy] = providers.Singleton(
        WorkflowManagerProxy,
        base_url=config.workflow_manager_url,
        verify_ssl=config.verify_ssl,
    )
    old_workflow_manager_proxy: providers.Singleton[legacy.IWorkflow] = providers.Singleton(
        OldWorkflowManagerProxy,
        base_url=config.workflow_manager_url,
        verify_ssl=config.verify_ssl,
    )
    old_ocr_proxy: providers.Singleton[legacy.IOCR] = providers.Singleton(
        OldOCRProxy, base_url=config.ocr_url, verify_ssl=config.verify_ssl
    )
    old_prototype_proxy: providers.Singleton[OldPrototypeProxy] = providers.Singleton(
        OldPrototypeProxy,
        base_url=config.prototype_url,
        verify_ssl=config.verify_ssl,
    )
    prototype_proxy: providers.Singleton[IBackwardCompatiblePrototypeProxy] = providers.Singleton(
        PrototypeProxy,
        base_url=config.prototype_url,
        verify_ssl=config.verify_ssl,
    )
    parsing_proxy: providers.Singleton[IParsingProxy] = providers.Singleton(
        ParsingProxy,
        base_url=config.parsing_url,
        verify_ssl=config.verify_ssl,
    )
    semantic_parsing_proxy: providers.Singleton[ISemanticParsingProxy] = providers.Singleton(
        SemanticParsingProxy,
        base_url=config.semantic_parsing_url,
        verify_ssl=config.verify_ssl,
    )
    old_enrichment_proxy: providers.Singleton[legacy.IEnrichment] = providers.Singleton(
        OldEnrichmentProxy,
        base_url=config.enrichment_url,
        verify_ssl=config.verify_ssl,
    )
    prompter_proxy: providers.Singleton[legacy.IPrompter] = providers.Singleton(
        PrompterProxy,
        base_url=config.prompter_url,
        verify_ssl=config.verify_ssl,
    )
    high_sparrow_proxy: providers.Singleton[IHighSparrowProxy] = providers.Singleton(
        HighSparrowProxy,
        base_url=config.high_sparrow_url,
        verify_ssl=config.verify_ssl,
    )
    unifier_proxy: providers.Singleton[IUnifierProxy] = providers.Singleton(
        UnifierProxy,
        base_url=config.unifier_url,
        verify_ssl=config.verify_ssl,
    )
    output_exporting_proxy: providers.Singleton[IOutputExportingProxy] = providers.Singleton(
        OutputExportingProxy,
        base_url=config.output_exporting_url,
        verify_ssl=config.verify_ssl,
    )
    ocr_proxy: providers.Singleton[IOCRProxy] = providers.Singleton(
        OCRProxy,
        base_url=config.ocr_url,
        verify_ssl=config.verify_ssl,
    )
    ai_fusion_proxy: providers.Singleton[IAIFusionProxy] = providers.Singleton(
        AIFusionProxy,
        base_url=config.ai_fusion_url,
        verify_ssl=config.verify_ssl,
    )
    litellm_proxy: providers.Singleton[ILiteLLMProxy] = providers.Singleton(
        LiteLLMProxy,
        base_url=config.litellm_url,
        api_key=config.litellm_api_key,
        verify_ssl=config.verify_ssl,
    )
    enrichment_proxy: providers.Singleton[IEnrichmentProxy] = providers.Singleton(
        EnrichmentProxy,
        base_url=config.enrichment_url,
        verify_ssl=config.verify_ssl,
    )
    template_proxy: providers.Singleton[ITemplateProxy] = providers.Singleton(
        TemplateProxy,
        base_url=config.template_url,
        verify_ssl=config.verify_ssl,
    )
    iam_proxy: providers.Singleton[IIAMProxy] = providers.Singleton(
        IAMProxy,
        base_url=config.iam_url,
        verify_ssl=config.verify_ssl,
    )
    groups_proxy: providers.Singleton[IGroupsProxy] = providers.Singleton(
        GroupsProxy,
        base_url=config.groups_url,
        verify_ssl=config.verify_ssl,
    )
    classification_proxy: providers.Singleton[IClassificationProxy] = providers.Singleton(
        ClassificationProxy,
        base_url=config.classification_url,
        verify_ssl=config.verify_ssl,
    )
    cloud_native_extraction_proxy: providers.Singleton[ICloudNativeExtractionProxy] = providers.Singleton(
        CloudNativeExtractionProxy,
        base_url=config.cloud_native_extraction_url,
        verify_ssl=config.verify_ssl,
    )
    storage_proxy: providers.Singleton[IStorageProxy] = providers.Singleton(
        StorageProxy,
        base_url=config.storage.url,
        verify_ssl=config.verify_ssl,
    )
    batch_proxy: providers.Singleton[IBatchProxy] = providers.Singleton(
        BatchProxy,
        base_url=config.files_batch_url,
        verify_ssl=config.verify_ssl,
    )
    splitting_proxy: providers.Singleton[ISplittingProxy] = providers.Singleton(
        SplittingProxy,
        base_url=config.splitting_url,
        verify_ssl=config.verify_ssl,
    )
    document_field_analytics_proxy: providers.Singleton[IDocumentFieldAnalyticsProxy] = providers.Singleton(
        AnalyticProxy,
        base_url=config.analytic_url,
        verify_ssl=config.verify_ssl,
    )
    event_relay_proxy: providers.Singleton[IEventRelayProxy] = providers.Singleton(
        EventRelayProxy,
        base_url=config.event_relay_url,
        verify_ssl=config.verify_ssl,
    )
    agentic_ai_proxy: providers.Singleton[IAgenticAIProxy] = providers.Singleton(
        AgenticAIProxy,
        base_url=config.agentic_ai_url,
        verify_ssl=config.verify_ssl,
    )
    agentic_ai_sse_proxy: providers.Singleton[IAgenticAISSEProxy] = providers.Singleton(
        AgenticAISSEProxy,
        base_url=config.agentic_ai_url,
    )
    file_proxy: providers.Singleton[IFileProxy] = providers.Singleton(
        FileProxy,
        base_url=config.file_url,
        verify_ssl=config.verify_ssl,
    )
    meta_agent_proxy: providers.Singleton[IMetaAgentProxy] = providers.Singleton(
        MetaAgentProxy,
        base_url=config.meta_agent_url,
        verify_ssl=config.verify_ssl,
    )


class Routers(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()
    domain_services = providers.DependenciesContainer()
    config = providers.Configuration()

    corleone_router: providers.Singleton[CorleoneRouter] = providers.Singleton(
        CorleoneRouter,
        client=external_services.corleone_generic_client,
        corleone_proxy=external_services.corleone_proxy,
        extraction_proxy=external_services.old_extraction_proxy,
        document_type_proxy=external_services.document_type_proxy_old,
        document_type_source_cache=domain_services.document_type_source_cache,
        document_type_code_cache=domain_services.document_type_code_cache,
        document_type_extraction_type_cache=domain_services.document_type_extraction_type_cache,
    )
    preprocess_router: providers.Singleton[PreprocessRouter] = providers.Singleton(
        PreprocessRouter,
        client=external_services.preprocess_generic_client,
        preprocess_proxy=external_services.preprocess_proxy,
        unifier_proxy=external_services.old_unifier_proxy,
        document_type_code_cache=domain_services.document_type_code_cache,
        document_type_source_cache=domain_services.document_type_source_cache,
    )
    validation_router: providers.Singleton[ValidationRouter] = providers.Singleton(
        ValidationRouter,
        client=external_services.validation_generic_client,
        high_sparrow_proxy=external_services.high_sparrow_proxy,
    )
    template_router: providers.Singleton[TemplateRouter] = providers.Singleton(
        TemplateRouter,
        client=external_services.template_generic_client,
        extraction_proxy=external_services.extraction_proxy,
    )
    prototype_router: providers.Singleton[PrototypeRouter] = providers.Singleton(
        PrototypeRouter,
        client=external_services.old_prototype_proxy,
        extraction_proxy=external_services.extraction_proxy,
        prototype_proxy=external_services.prototype_proxy,
    )
    document_type_router: providers.Singleton[DocumentTypeRouter] = providers.Singleton(
        DocumentTypeRouter,
        client=external_services.document_type_proxy_old,
        extraction_proxy=external_services.extraction_proxy,
    )
    document_router: providers.Singleton[DocumentRouter] = providers.Singleton(
        DocumentRouter,
        client=external_services.document_generic_client,
        document_proxy=external_services.old_document_proxy,
        corleone_proxy=external_services.corleone_proxy,
        document_type_proxy=external_services.document_type_proxy_old,
        workflow_manager_proxy=external_services.old_workflow_manager_proxy,
        document_type_source_cache=domain_services.document_type_source_cache,
        document_type_code_cache=domain_services.document_type_code_cache,
        document_type_extraction_type_cache=domain_services.document_type_extraction_type_cache,
        workflow_v2=config.workflow_v2,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    document_type_source_cache: providers.Singleton[TTLCache] = providers.Singleton(
        TTLCache,
        ttl=config.cache_settings.document_type_source_cache_ttl,
        maxsize=config.cache_settings.document_type_source_cache_max_size,
    )

    document_type_code_cache: providers.Singleton[TTLCache] = providers.Singleton(
        TTLCache,
        ttl=config.cache_settings.document_type_code_cache_ttl,
        maxsize=config.cache_settings.document_type_code_cache_max_size,
    )

    document_type_extraction_type_cache: providers.Singleton[TTLCache] = providers.Singleton(
        TTLCache,
        ttl=config.cache_settings.document_type_source_cache_ttl,
        maxsize=config.cache_settings.document_type_source_cache_max_size,
    )
    rarely_updatable_cache: providers.Singleton[TTLCache] = providers.Singleton(
        TTLCache,
        ttl=config.cache_settings.rarely_updatable_cache_ttl,
        maxsize=config.cache_settings.rarely_updatable_cache_max_size,
    )


class Tools(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()

    ocr: providers.Singleton[OCRService] = providers.Singleton(
        OCRService,
        ocr_proxy=external_services.ocr_proxy,
    )

    parsing: providers.Singleton[ParsingToolsService] = providers.Singleton(
        ParsingToolsService,
        parsing_proxy=external_services.parsing_proxy,
    )

    ai_fusion: providers.Singleton[AIFusionService] = providers.Singleton(
        AIFusionService,
        ai_fusion_proxy=external_services.ai_fusion_proxy,
    )

    litellm: providers.Singleton[LiteLLMService] = providers.Singleton(
        LiteLLMService,
        litellm_proxy=external_services.litellm_proxy,
    )


class Application(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()
    domain_services = providers.DependenciesContainer()

    document_type_oldest: providers.Singleton[legacy.DocumentTypeOldService] = providers.Singleton(
        legacy.DocumentTypeOldService,
        external_services.corleone_proxy,
        external_services.document_type_proxy_old,
        domain_services.document_type_source_cache,
    )
    document_type_old: providers.Singleton[legacy.DocumentTypeService] = providers.Singleton(
        legacy.DocumentTypeService,
        document_type_proxy=external_services.document_type_proxy_v1,
        extraction_proxy=external_services.extraction_proxy,
    )
    document_type: providers.Singleton[DocumentTypeService] = providers.Singleton(
        DocumentTypeService,
        high_sparrow_proxy=external_services.high_sparrow_proxy,
        extraction_proxy=external_services.extraction_proxy,
        prototype_proxy=external_services.prototype_proxy,
        document_type_proxy=external_services.document_type_proxy_v5,
        output_exporting_proxy=external_services.output_exporting_proxy,
        enrichment_proxy=external_services.enrichment_proxy,
        template_proxy=external_services.template_proxy,
        workflow_manager_proxy=external_services.workflow_manager_proxy,
        cloud_native_extraction_proxy=external_services.cloud_native_extraction_proxy,
        classification_proxy=external_services.classification_proxy,
        ai_fusion_proxy=external_services.ai_fusion_proxy,
        parsing_proxy=external_services.parsing_proxy,
        unifier_proxy=external_services.unifier_proxy,
    )
    document_old: providers.Singleton[legacy.DocumentService] = providers.Singleton(
        legacy.DocumentService,
        document_proxy=external_services.old_document_proxy,
        corleone_proxy=external_services.corleone_proxy,
        document_type_proxy=external_services.document_type_proxy_old,
        ocr_proxy=external_services.old_ocr_proxy,
        rarely_updatable_cache=domain_services.rarely_updatable_cache,
        document_type_source_cache=domain_services.document_type_source_cache,
        document_type_code_cache=domain_services.document_type_code_cache,
        document_type_extraction_type_cache=domain_services.document_type_extraction_type_cache,
    )
    document: providers.Singleton[DocumentService] = providers.Singleton(
        DocumentService,
        document_proxy=external_services.document_proxy,
        high_sparrow_proxy=external_services.high_sparrow_proxy,
        unifier_proxy=external_services.unifier_proxy,
        parsing_proxy=external_services.parsing_proxy,
        semantic_parsing_proxy=external_services.semantic_parsing_proxy,
        output_exporting_proxy=external_services.output_exporting_proxy,
        ai_fusion_proxy=external_services.ai_fusion_proxy,
        workflow_manager_proxy=external_services.workflow_manager_proxy,
        enrichment_proxy=external_services.enrichment_proxy,
        extraction_proxy=external_services.extraction_proxy,
    )
    workflow_old: providers.Singleton[legacy.WorkflowService] = providers.Singleton(
        legacy.WorkflowService,
        workflow_manager_proxy=external_services.old_workflow_manager_proxy,
    )
    workflow: providers.Singleton[WorkflowService] = providers.Singleton(
        WorkflowService,
        workflow_manager_proxy=external_services.workflow_manager_proxy,
    )
    prototype: providers.Singleton[legacy.PrototypeService] = providers.Singleton(
        legacy.PrototypeService,
        prototype_proxy=external_services.prototype_proxy,
        unifier_proxy=external_services.old_unifier_proxy,
        parsing_proxy=external_services.parsing_proxy,
    )
    parsing_old: providers.Singleton[legacy.ParsingService] = providers.Singleton(
        legacy.ParsingService,
        parsing_proxy=external_services.parsing_proxy,
    )
    parsing: providers.Singleton[ParsingService] = providers.Singleton(
        ParsingService,
        parsing_proxy=external_services.parsing_proxy,
    )
    enrichment: providers.Singleton[legacy.EnrichmentService] = providers.Singleton(
        legacy.EnrichmentService,
        enrichment_proxy=external_services.old_enrichment_proxy,
    )
    prompter: providers.Singleton[legacy.PrompterService] = providers.Singleton(
        legacy.PrompterService,
        prompter_proxy=external_services.prompter_proxy,
    )
    extraction_old: providers.Singleton[legacy.ExtractionService] = providers.Singleton(
        legacy.ExtractionService,
        extraction_proxy=external_services.extraction_proxy,
    )
    extraction: providers.Singleton[ExtractionService] = providers.Singleton(
        ExtractionService,
        extraction_proxy=external_services.extraction_proxy,
    )

    tools: providers.Container[Tools] = providers.Container(
        Tools,
        external_services=external_services,
    )

    iam: providers.Singleton[IAMService] = providers.Singleton(
        IAMService,
        proxy=external_services.iam_proxy,
    )

    group: providers.Singleton[GroupService] = providers.Singleton(
        GroupService,
        groups_proxy=external_services.groups_proxy,
        classification_proxy=external_services.classification_proxy,
        splitter_proxy=external_services.splitting_proxy,
    )

    document_field_analytics: providers.Singleton[DocumentFieldAnalyticsService] = providers.Singleton(
        DocumentFieldAnalyticsService,
        document_field_analytics_proxy=external_services.document_field_analytics_proxy,
        extraction_proxy=external_services.extraction_proxy,
    )

    storage: providers.Singleton[StorageService] = providers.Singleton(
        StorageService,
        proxy=external_services.storage_proxy,
    )

    batch: providers.Singleton[BatchService] = providers.Singleton(
        BatchService,
        batch_proxy=external_services.batch_proxy,
    )
    splitter: providers.Singleton[SplittingService] = providers.Singleton(
        SplittingService,
        splitter_proxy=external_services.splitting_proxy,
    )
    event_relay: providers.Singleton[EventRelayService] = providers.Singleton(
        EventRelayService,
        event_relay_proxy=external_services.event_relay_proxy,
    )
    service_discovery: providers.Singleton[ServiceDiscovery] = providers.Singleton(
        ServiceDiscovery,
    )
    agentic_ai: providers.Singleton[AgenticAIService] = providers.Singleton(
        AgenticAIService,
        agentic_ai_proxy=external_services.agentic_ai_proxy,
        agentic_ai_sse_proxy=external_services.agentic_ai_sse_proxy,
    )
    file: providers.Singleton[FileService] = providers.Singleton(
        FileService,
        file_proxy=external_services.file_proxy,
        unifier_proxy=external_services.unifier_proxy,
        parsing_proxy=external_services.parsing_proxy,
    )
    meta_agent: providers.Singleton[MetaAgentService] = providers.Singleton(
        MetaAgentService,
        meta_agent_proxy=external_services.meta_agent_proxy,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: providers.Container[Core] = providers.Container(Core, config=config)

    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
    )

    routers: providers.Container[Routers] = providers.Container(
        Routers,
        external_services=external_services,
        domain_services=domain_services,
        config=config,
    )

    application: providers.Container[Application] = providers.Container(
        Application,
        external_services=external_services,
        domain_services=domain_services,
    )
