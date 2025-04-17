import os
from rara_subject_indexer.utils.downloader import Downloader
from rara_subject_indexer.indexers.keyword_indexers.indexers import (
    TopicIndexer, TimeIndexer, GenreIndexer, NERKeywordIndexer, 
    UDCIndexer, CategoryIndexer, UDC2Indexer
)
from rara_subject_indexer.utils.text_preprocessor import (
    TextPreprocessor, ProcessedText
)
from rara_subject_indexer.ner.ner_subject_indexer import NERIndexer
from rara_subject_indexer.exceptions import InvalidLanguageException, MissingDataException
from rara_subject_indexer.config import (
    NERMethod, ModelArch, KeywordType, 
    ALLOWED_METHODS_MAP, SUPPORTED_LANGUAGES, POSTAGS_TO_IGNORE,
    DEFAULT_KEYWORD_METHOD_MAP, DEFAULT_KEYWORD_TYPES,
    TOPIC_KEYWORD_CONFIG, GENRE_KEYWORD_CONFIG, TIME_KEYWORD_CONFIG,
    CATEGORY_CONFIG, NER_KEYWORDS, UDC_CONFIG, UDC2_CONFIG, NER_CONFIG,
    LOGGER, NER_DATA_DIR, OMIKUJI_DATA_DIR, GOOGLE_DRIVE_URL, THRESHOLD_CONFIG
)
from typing import NoReturn, List, Dict
from time import time
from collections import defaultdict



intersection = lambda x, y: set(x).intersection(set(y))
has_intersection = lambda x, y: bool(intersection(x,y))
load_keyword_model =  lambda x, y: bool(
    x in y or x == KeywordType.NER and has_intersection(NER_KEYWORDS, y)
)
intersection_size = lambda x, y: len(intersection(x,y))
difference = lambda x, y: set(x) - set(y)

class RaraSubjectIndexer:
    def __init__(
        self, 
        methods: dict = DEFAULT_KEYWORD_METHOD_MAP,
        keyword_types: list = DEFAULT_KEYWORD_TYPES,
        topic_config: dict = TOPIC_KEYWORD_CONFIG,
        time_config: dict = TIME_KEYWORD_CONFIG,
        genre_config: dict = GENRE_KEYWORD_CONFIG,
        category_config: dict = CATEGORY_CONFIG,
        udc_config: dict = UDC_CONFIG,
        udc2_config: dict = UDC2_CONFIG,
        ner_config: dict = NER_CONFIG
     ) -> NoReturn:

        self.methods = methods
        self.keyword_types = keyword_types

        self.indexers_map = {
            KeywordType.TOPIC: {"class": TopicIndexer, "config": topic_config},
            KeywordType.TIME: {"class": TimeIndexer, "config": time_config},
            KeywordType.GENRE: {"class": GenreIndexer, "config": genre_config},
            KeywordType.NER: {"class": NERKeywordIndexer, "config": ner_config},
            KeywordType.UDK: {"class": UDCIndexer, "config": udc_config},
            KeywordType.UDK2: {"class": UDC2Indexer, "config": udc2_config},
            KeywordType.CATEGORY: {"class": CategoryIndexer, "config": category_config},
        }
            
        self.__text_preprocessor: TextPreprocessor = TextPreprocessor()
        self.__text: ProcessedText | None = None
        self.__keywords: List[dict] = []
        
        self.indexers = {
            keyword_type: self._load_indexers(keyword_type)
            for keyword_type in self.indexers_map
            if load_keyword_model(keyword_type, self.keyword_types)
        }
        
    def _load_indexers(self, keyword_type: str):
        indexer_info = self.indexers_map.get(keyword_type)
        indexer_class = indexer_info.get("class")
        indexer_config = indexer_info.get("config")
        LOGGER.info(
            f"Loading indexers for keyword type {keyword_type}: " \
            f"{self.methods.get(keyword_type)}."
        )
        indexers = {
            model_arch: indexer_class(
                model_arch=model_arch,
                config=indexer_config
            )
            for model_arch in self.methods.get(keyword_type)
        }
        return indexers
    
    @staticmethod
    def download_resources(drive_url: str = GOOGLE_DRIVE_URL, 
            gliner: bool = True, stanza: bool = True, omikuji: bool = True
    ) -> NoReturn:
        if stanza or gliner:
            NERIndexer.download_model_resources(
                resource_dir=NER_DATA_DIR, 
                gliner=gliner,
                stanza=stanza
            )
        if omikuji:
            RaraSubjectIndexer.download_models_from_gdrive(
                drive_url=drive_url,
                output_dir=OMIKUJI_DATA_DIR
            )
         
    
    @staticmethod
    def download_models_from_gdrive(drive_url: str, output_dir: str) -> NoReturn:
        """ Downloads all files from a Google drive folder. NB! Expects 
        the files to be .zips.
        
        Parameters
        -----------
        drive_url: str
            Google Drive folder full URL or folder ID.
        output_dir: str
            Directory, where to save the models.
            
        """
        gdrive_downloader = Downloader(
            drive_url=drive_url, 
            output_dir=output_dir
        )
        gdrive_downloader.download_folder()
        
    def _filter_ner_keywords(self, keywords: List[dict]) -> List[dict]:
        """ Filters out NER-based keyword types that were
        not chosen for extraction.
        
        Parameters
        -----------
        keywords: List[dict]
            NER-based keywords.
        
        Returns
        ----------
        List[dict]
            Extracted NER keywords.
        """
        if intersection_size(NER_KEYWORDS, self.keyword_types) < len(NER_KEYWORDS):
            LOGGER.debug(
                f"Filtering out the following NER-based keywords as " \
                f"they were not selected for extraction: " \
                f"{difference(NER_KEYWORDS, self.keyword_types)}."
            )
            filtered_keywords = []
            for keyword in keywords:
                if keyword.get("entity_type") in self.keyword_types:
                    filtered_keywords.append(keyword)
        else:
            filtered_keywords = keywords
        return filtered_keywords
    
    def _keywords_to_dict(self, keywords: List[dict]) -> Dict[str, Dict[str, List]]:
        keywords_dict = defaultdict(lambda: defaultdict(list))
        for keyword in keywords:
            keyword_type = keyword.get("entity_type")
            model_arch = keyword.get("model_arch")
            keywords_dict[keyword_type][model_arch].append(keyword)
        return keywords_dict
        
    
    def _filter_by_score_and_count(self, 
        keywords, threshold_config: dict, min_score: float, max_count: int
    ):
        keywords_dict = self._keywords_to_dict(keywords)
        filtered_keywords = []

        for keyword_type, model_arches in keywords_dict.items():
            for model_arch, keywords in model_arches.items():
                _filtered_keywords = []

                keywords = keywords_dict[keyword_type][model_arch]

                scores = threshold_config.get(keyword_type, {}).get(model_arch, {})

                _min_score = scores.get("min_score", min_score)
                _max_count = scores.get("max_count", max_count)

                for keyword in keywords:
                    if keyword.get("score") >= _min_score:
                        _filtered_keywords.append(keyword)

                filtered_keywords.extend(_filtered_keywords[:_max_count])
        return filtered_keywords
    
    def _check_relevant_data_exists(self):
        if not os.path.exists(OMIKUJI_DATA_DIR) or not os.path.exists(NER_DATA_DIR):
            return False
        elif not os.listdir(OMIKUJI_DATA_DIR) or not os.listdir(NER_DATA_DIR):
            return False
        return True
            
        
    def apply_indexers(self, text: str, lang: str = "", 
           min_score: float = 0.0, min_count: int = 1, 
           max_count: int = 10, threshold_config: dict = THRESHOLD_CONFIG,
           flat: bool = True
    ):  
        data_exists = self._check_relevant_data_exists()
        if not data_exists:
            error_msg = (
                f"Missing relevant Omikuji models from '{OMIKUJI_DATA_DIR}' " \
                f"and/or NER models from '{NER_DATA_DIR}'. Please make " \
                f"sure to download them first!"
            )
            LOGGER.error(error_msg)
            raise MissingDataException(error_msg)
        
        if self.__text and text == self.__text.original_text:
            keywords = self.__keywords
            
        else:
            if not lang:
                lang = TextPreprocessor.detect_language(text)

            if lang not in SUPPORTED_LANGUAGES:
                error_msg = (
                    f"The text appears to be in language '{lang}', "
                    f"which is not supported. Supported " \
                    f"languages are: {SUPPORTED_LANGUAGES}."
                )
                LOGGER.error(error_msg)
                raise InvalidLanguageException(error_msg)
                
            keywords = []
            
            processed_text = ProcessedText(
                text=text, 
                lang_code=lang,
                text_preprocessor=self.__text_preprocessor
            )
            durations = []
            for keyword_type in self.indexers:
                for model_arch, indexer in self.indexers[keyword_type].items():
                    LOGGER.info(
                        f"Applying indexer '{indexer.__class__.__name__}' " \
                        f"with model arch '{model_arch}' for keyword type " \
                        f"'{keyword_type}'"
                    )
                    start = time()
                    _keywords = indexer.find_keywords(
                        text=processed_text,
                        lang=lang,
                        min_score=min_score,
                        min_count=min_count,
                        max_count=max_count,
                        lemmatize=False
                    )
                    duration = time() - start

                    if keyword_type == KeywordType.NER:
                        _keywords = self._filter_ner_keywords(_keywords)
                    
                    keywords.extend(_keywords)
                    durations.append(
                        {
                            "duration": round(duration, 5), 
                            "model_arch": model_arch.value, 
                            "keyword_type": keyword_type.value
                        }
                    )
            self.__text = processed_text
            self.__keywords = keywords

            
        # Filtering
        final_keywords = self._filter_by_score_and_count(
            keywords, threshold_config, min_score, max_count
        )
        
        if not flat:
            nested_keywords = []
            keywords_dict = self._keywords_to_dict(final_keywords)
            for keyword_type, model_arches in keywords_dict.items():
                for model_arch, _keywords in model_arches.items():
                    for kw in _keywords:
                        kw.pop("model_arch")
                        kw.pop("entity_type")
                    keyword_batch = {
                        "keyword_type": keyword_type,
                        "model_arch": model_arch,
                        "keywords": _keywords
                    }
                    nested_keywords.append(keyword_batch)
            final_keywords = nested_keywords
                    
                    
        results = {"keywords": final_keywords, "durations": durations}    
        return results