"""
資料準備工具集初始化文件

提供 CLI 工具集的入口點和主要功能
"""
from .cli import (
    clean_coach_responses,
    clean_video_transcripts,
    extract_knowledge_from_coach_responses,
    validate_extracted_knowledge,
    main
)
from .utils import (
    clean_text,
    extract_keywords,
    validate_json_structure,
    format_timestamp,
    detect_language,
    split_into_segments,
    merge_segments,
    normalize_units,
    normalize_dates
)
from .extractors import (
    extract_symptoms_from_coach_response,
    extract_practice_suggestions_from_coach_response,
    create_structured_knowledge_representation,
    extract_knowledge_from_coach_response,
    extract_knowledge_from_video_transcript
)
from .validators import (
    validate_symptom_data,
    validate_practice_card_data,
    validate_symptom_practice_mapping_data,
    validate_feedback_data,
    generate_validation_report
)
from .analyzer import (
    analyze_extracted_knowledge,
    validate_knowledge_quality,
    check_data_consistency,
    generate_quality_report,
    calculate_quality_score
)
from .importer import (
    import_knowledge_to_database,
    import_knowledge_from_json_file,
    parse_knowledge_from_json,
    validate_before_import,
    generate_import_report
)
from .models import (
    SymptomDescription,
    PracticeSuggestion,
    KnowledgeStructure,
    ExtractedKnowledge,
    ValidationReport,
    SymptomValidationResult,
    PracticeCardValidationResult,
    SymptomPracticeMappingValidationResult,
    FeedbackValidationResult,
    UserPreferenceAnalysis,
    SymptomFeedbackAnalysis,
    PracticeCardFeedbackAnalysis,
    OverallFeedbackAnalytics
)

__all__ = [
    "clean_coach_responses",
    "clean_video_transcripts",
    "extract_knowledge_from_coach_responses",
    "validate_extracted_knowledge",
    "main",
    "clean_text",
    "extract_keywords",
    "validate_json_structure",
    "format_timestamp",
    "detect_language",
    "split_into_segments",
    "merge_segments",
    "normalize_units",
    "normalize_dates",
    "extract_symptoms_from_coach_response",
    "extract_practice_suggestions_from_coach_response",
    "create_structured_knowledge_representation",
    "extract_knowledge_from_coach_response",
    "extract_knowledge_from_video_transcript",
    "validate_symptom_data",
    "validate_practice_card_data",
    "validate_symptom_practice_mapping_data",
    "validate_feedback_data",
    "generate_validation_report",
    "analyze_extracted_knowledge",
    "validate_knowledge_quality",
    "check_data_consistency",
    "generate_quality_report",
    "calculate_quality_score",
    "import_knowledge_to_database",
    "import_knowledge_from_json_file",
    "parse_knowledge_from_json",
    "validate_before_import",
    "generate_import_report",
    "SymptomDescription",
    "PracticeSuggestion",
    "KnowledgeStructure",
    "ExtractedKnowledge",
    "ValidationReport",
    "SymptomValidationResult",
    "PracticeCardValidationResult",
    "SymptomPracticeMappingValidationResult",
    "FeedbackValidationResult",
    "UserPreferenceAnalysis",
    "SymptomFeedbackAnalysis",
    "PracticeCardFeedbackAnalysis",
    "OverallFeedbackAnalytics"
]