USE dataengine;

CREATE TABLE IF NOT EXISTS t_clean_template
(
    id          varchar(64) primary key not null unique,
    name        varchar(64),
    description varchar(256),
    created_at  timestamp default current_timestamp,
    updated_at  timestamp default current_timestamp,
    created_by  varchar(256)
);

CREATE TABLE IF NOT EXISTS t_clean_task
(
    id                varchar(64) primary key,
    name              varchar(64),
    description       varchar(256),
    status            varchar(256),
    src_dataset_id    varchar(64),
    src_dataset_name  varchar(64),
    dest_dataset_id   varchar(64),
    dest_dataset_name varchar(64),
    before_size       bigint,
    after_size        bigint,
    created_at        timestamp default current_timestamp,
    started_at        timestamp,
    finished_at       timestamp,
    created_by        varchar(256)
);

CREATE TABLE IF NOT EXISTS t_operator_instance
(
    instance_id       varchar(256),
    operator_id       varchar(256),
    op_index          int,
    settings_override text,
    PRIMARY KEY (instance_id, operator_id, op_index)
);

CREATE TABLE IF NOT EXISTS t_clean_result
(
    instance_id varchar(64),
    src_file_id varchar(64),
    dest_file_id varchar(64),
    src_name    varchar(256),
    dest_name    varchar(256),
    src_type    varchar(256),
    dest_type    varchar(256),
    src_size    bigint,
    dest_size    bigint,
    status      varchar(256),
    result      TEXT,
    primary key (instance_id, dest_file_id)
);

INSERT IGNORE INTO t_clean_template(id, name, description)
VALUES ('ac2f2582-a990-11f0-9768-00155d09c825', '空模板', '空模板'),
       ('fb6d0d76-a990-11f0-92db-00155d09c825', '测试模板', '测试模板'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'text文本清洗模板', 'text文本清洗模板');

INSERT IGNORE INTO t_operator_instance(instance_id, operator_id, op_index, settings_override)
VALUES ('fb6d0d76-a990-11f0-92db-00155d09c825', 'TextFormatter', 1, '{}'),
       ('fb6d0d76-a990-11f0-92db-00155d09c825', 'FileExporter', 2, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'TextFormatter', 1, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithShortOrLongLengthFilter', 2, '{"fileLength": {"name": "文档字数", "name_en": "Words", "description": "过滤字数不在指定范围内的文档，如[10,10000000]。若输入为空，则不对字数上/下限做限制。", "description_en": "Filters out files whose number of words is not within the range you set, for example, [10,10000000]. If left blank, the minimum and maximum number of words have no limit.", "type": "range", "properties": [{"name": "fileMinimumLength", "type": "inputNumber", "defaultVal": 10, "min": 0, "max": 10000000000000000, "step": 1}, {"name": "fileMaximumLength", "type": "inputNumber", "defaultVal": 10000000, "min": 0, "max": 10000000000000000, "step": 1}]}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighRepeatWordRateFilter', 3, '{"repeatWordRatio": {"name": "文档字重复率", "name_en": "Word Repetition Rate", "description": "某个字的统计数/文档总字数 > 设定值，该文档被去除。", "description_en": "Filters out files that meet the formula: Number of times a word occurs/Totalnumber of words > Value you set.", "type": "slider", "defaultVal": 0.5, "min": 0, "max": 1, "step": 0.1}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighRepeatPhraseRateFilter', 4, '{"repeatPhraseRatio": {"name": "文档词重复率", "name_en": "Phrase Repetition Rate", "description": "某个词的统计数/文档总词数 > 设定值，该文档被去除。", "description_en": "Filters out files that meet the formula: Number of times a phrase occurs/Total number of phrases > Value you set.", "type": "slider", "defaultVal": 0.5, "min": 0, "max": 1, "step": 0.1}, "hitStopwords": {"name": "去除停用词", "name_en": "Remove Stop Words", "description": "统计重复词时，选择是否要去除停用词。", "description_en": "Whether to remove stop words when collecting repeated phrases.", "type": "switch", "defaultVal": false, "required": true, "checkedLabel": "去除", "checkedLabel_en": "Yes", "unCheckedLabel": "不去除", "unCheckedLabel_en": "No"}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighSpecialCharRateFilter', 5, '{"specialCharRatio": {"name": "文档特殊字符率", "name_en": "Special Character Rate", "description": "特殊字符的统计数/文档总字数 > 设定值，该文档被去除。", "description_en": "Filters out files that meet the following formula: Number of special characters/Total number of words > Value you set.", "type": "slider", "defaultVal": 0.3, "min": 0, "max": 1, "step": 0.1}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithManySensitiveWordsFilter', 6, '{"sensitiveWordsRate": {"name": "文档敏感词率", "name_en": "Sensitive Phrase Rate", "description": "敏感词的字数/文档总字数 > 设定值，该文档被去除。", "description_en": "Filters out files that meet the following formula: Number of words in sensitive phrases/Total number of words > Value you set.", "type": "slider", "defaultVal": 0.01, "min": 0, "max": 1, "step": 0.01}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'UnicodeSpaceCleaner', 7, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'ExtraSpaceCleaner', 8, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FullWidthCharacterCleaner', 9, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'InvisibleCharactersCleaner', 10, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'ContentCleaner', 11, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'LegendCleaner', 12, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'EmojiCleaner', 13, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'HtmlTagCleaner', 14, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'TraditionalChineseCleaner', 15, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'GrableCharactersCleaner', 16, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'XMLTagCleaner', 17, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'DuplicateSentencesFilter', 18, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'DuplicateFilesFilter', 19, '{"fileDuplicateThreshold": {"name": "文档相似度", "name_en": "File Similarity", "description": "基于MinHash算法和Jaccard相似度，计算当前文档与数据集中其它文档相似性，超过设定值，该文档被去除。", "description_en": "Based on MinHash and Jaccard index, the system calculates the similarity between the current file and other files in the dataset, and filters out the file if its similarity exceeds the value you set.", "type": "slider", "defaultVal": 0.5, "min": 0, "max": 1, "step": 0.1}}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'SexualAndViolentWordCleaner', 20, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'PoliticalWordCleaner', 21, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedPhoneNumber', 22, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedCreditCardNumber', 23, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'EmailNumberCleaner', 24, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedIpAddress', 25, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedIdNumber', 26, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedUrlCleaner', 27, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileExporter', 28, '{}');
