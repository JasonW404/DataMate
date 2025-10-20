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
    instance_id varchar(64) primary key,
    src_file_id varchar(64),
    dst_file_id varchar(64),
    src_name    varchar(256),
    src_type    varchar(256),
    src_size    bigint,
    dst_size    bigint,
    status      varchar(256)
);

INSERT IGNORE INTO t_clean_template(id, name, description)
VALUES ('ac2f2582-a990-11f0-9768-00155d09c825', '空模板', '空模板'),
       ('fb6d0d76-a990-11f0-92db-00155d09c825', '测试模板', '测试模板'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'text文本清洗模板', 'text文本清洗模板');

INSERT IGNORE INTO t_operator_instance(instance_id, operator_id, op_index, settings_override)
VALUES ('fb6d0d76-a990-11f0-92db-00155d09c825', 'TextFormatter', 1, '{}'),
       ('fb6d0d76-a990-11f0-92db-00155d09c825', 'FileExporter', 2, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'TextFormatter', 1, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithShortOrLongLengthFilter', 2, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighRepeatWordRateFilter', 3, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighRepeatPhraseRateFilter', 4, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithHighSpecialCharRateFilter', 5, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileWithManySensitiveWordsFilter', 6, '{}'),
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
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'DuplicateFilesFilter', 19, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'SexualAndViolentWordCleaner', 20, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'PoliticalWordCleaner', 21, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedPhoneNumber', 22, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedCreditCardNumber', 23, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'EmailNumberCleaner', 24, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedIpAddress', 25, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedIdNumber', 26, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'AnonymizedUrlCleaner', 27, '{}'),
       ('26ae585c-8310-4679-adc0-e53215e6e69b', 'FileExporter', 28, '{}');
