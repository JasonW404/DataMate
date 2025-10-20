USE dataengine;

CREATE TABLE IF NOT EXISTS t_operator
(
  id          varchar(64) primary key,
  name        varchar(64),
  description varchar(256),
  version     varchar(256),
  inputs      varchar(256),
  outputs     varchar(256),
  runtime     text,
  settings    text,
  file_name   text,
  is_star     bool,
  created_at   timestamp default current_timestamp,
  updated_at   timestamp default current_timestamp
);

CREATE TABLE IF NOT EXISTS t_operator_category
(
  id        int primary key auto_increment,
  name      varchar(64),
  type      varchar(64),
  parent_id int
);

CREATE TABLE IF NOT EXISTS t_operator_category_relation
(
  id int primary key auto_increment,
  category_id int,
  operator_id varchar(64)
);

CREATE OR REPLACE VIEW v_operator AS
SELECT
  o.id AS operator_id,
  o.name AS operator_name,
  description,
  version,
  inputs,
  outputs,
  runtime,
  settings,
  is_star,
  created_at,
  updated_at,
  toc.id AS category_id,
  toc.name AS category_name
FROM t_operator_category_relation tocr
LEFT JOIN t_operator o ON tocr.operator_id = o.id
LEFT JOIN t_operator_category toc ON tocr.category_id = toc.id;

INSERT IGNORE INTO t_operator_category(id, name, type, parent_id) VALUES
(1, 'modal', 'predefined', 0),
(2, 'language', 'predefined', 0),
(3, 'text', 'predefined', 1),
(4, 'image', 'predefined', 1),
(5, 'audio', 'predefined', 1),
(6, 'video', 'predefined', 1),
(7, 'multimodal', 'predefined', 1),
(8, 'python', 'predefined', 2),
(9, 'java', 'predefined', 2);

INSERT IGNORE INTO t_operator
  (id, name, description, version, inputs, outputs, runtime, settings, file_name, is_star) VALUES
('TextFormatter', 'TXT文本抽取', '', '1.0.0', 'text', 'text', '', '', '', false),
('FileExporter', '落盘算子', '', '1.0.0', 'all', 'all', '', '', '', false),
('FileWithHighRepeatPhraseRateFilter', '文档词重复率检查', '', '1.0.0', 'text', 'text', '', '', '', false),
('FileWithHighRepeatWordRateFilter', '文档字重复率检查', '', '1.0.0', 'text', 'text', '', '', '', false),
('FileWithHighSpecialCharRateFilter', '文档特殊字符率检查', '', '1.0.0', 'text', 'text', '', '', '', false),
('DuplicateFilesFilter', '相似文档去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('FileWithManySensitiveWordsFilter', '文档敏感词率检查', '', '1.0.0', 'text', 'text', '', '', '', false),
('FileWithShortOrLongLengthFilter', '文档字数检查', '', '1.0.0', 'text', 'text', '', '', '', false),
('ContentCleaner', '文档目录去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('AnonymizedCreditCardNumber', '信用卡号匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('EmailNumberCleaner', '邮件地址匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('EmojiCleaner', '文档表情去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('ExtraSpaceCleaner', '多余空格去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('FullWidthCharacterCleaner', '全角转半角', '', '1.0.0', 'text', 'text', '', '', '', false),
('GrableCharactersCleaner', '文档乱码去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('HtmlTagCleaner', 'HTML标签去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('AnonymizedIdNumber', '身份证号匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('InvisibleCharactersCleaner', '不可见字符去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('AnonymizedIpAddress', 'IP地址匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('LegendCleaner', '图注表注去除', '', '1.0.0', 'text', 'text', '', '', '', false),
('AnonymizedPhoneNumber', '电话号码匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('PoliticalWordCleaner', '政治文本匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('DuplicateSentencesFilter', '文档局部内容去重', '', '1.0.0', 'text', 'text', '', '', '', false),
('SexualAndViolentWordCleaner', '暴力色情文本匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('TraditionalChineseCleaner', '繁体转简体', '', '1.0.0', 'text', 'text', '', '', '', false),
('UnicodeSpaceCleaner', '空格标准化', '', '1.0.0', 'text', 'text', '', '', '', false),
('AnonymizedUrlCleaner', 'URL网址匿名化', '', '1.0.0', 'text', 'text', '', '', '', false),
('XMLTagCleaner', 'XML标签去除', '', '1.0.0', 'text', 'text', '', '', '', false);

INSERT IGNORE INTO t_operator_category_relation(category_id, operator_id) VALUES
(3, 'TextFormatter'),
(7, 'FileExporter'),
(8, 'TextFormatter'),
(8, 'FileExporter'),
(3, 'FileWithShortOrLongLengthFilter'),
(3, 'FileWithHighRepeatPhraseRateFilter'),
(3, 'FileWithHighRepeatWordRateFilter'),
(3, 'FileWithHighSpecialCharRateFilter'),
(3, 'FileWithManySensitiveWordsFilter'),
(3, 'DuplicateFilesFilter'),
(3, 'DuplicateSentencesFilter'),
(3, 'AnonymizedCreditCardNumber'),
(3, 'AnonymizedIdNumber'),
(3, 'AnonymizedIpAddress'),
(3, 'AnonymizedPhoneNumber'),
(3, 'AnonymizedUrlCleaner'),
(3, 'HtmlTagCleaner'),
(3, 'XMLTagCleaner'),
(3, 'ContentCleaner'),
(3, 'EmailNumberCleaner'),
(3, 'EmojiCleaner'),
(3, 'ExtraSpaceCleaner'),
(3, 'FullWidthCharacterCleaner'),
(3, 'GrableCharactersCleaner'),
(3, 'InvisibleCharactersCleaner'),
(3, 'LegendCleaner'),
(3, 'PoliticalWordCleaner'),
(3, 'SexualAndViolentWordCleaner'),
(3, 'TraditionalChineseCleaner'),
(3, 'UnicodeSpaceCleaner'),
(8, 'FileWithShortOrLongLengthFilter'),
(8, 'FileWithHighRepeatPhraseRateFilter'),
(8, 'FileWithHighRepeatWordRateFilter'),
(8, 'FileWithHighSpecialCharRateFilter'),
(8, 'FileWithManySensitiveWordsFilter'),
(8, 'DuplicateFilesFilter'),
(8, 'DuplicateSentencesFilter'),
(8, 'AnonymizedCreditCardNumber'),
(8, 'AnonymizedIdNumber'),
(8, 'AnonymizedIpAddress'),
(8, 'AnonymizedPhoneNumber'),
(8, 'AnonymizedUrlCleaner'),
(8, 'HtmlTagCleaner'),
(8, 'XMLTagCleaner'),
(8, 'ContentCleaner'),
(8, 'EmailNumberCleaner'),
(8, 'EmojiCleaner'),
(8, 'ExtraSpaceCleaner'),
(8, 'FullWidthCharacterCleaner'),
(8, 'GrableCharactersCleaner'),
(8, 'InvisibleCharactersCleaner'),
(8, 'LegendCleaner'),
(8, 'PoliticalWordCleaner'),
(8, 'SexualAndViolentWordCleaner'),
(8, 'TraditionalChineseCleaner'),
(8, 'UnicodeSpaceCleaner');
