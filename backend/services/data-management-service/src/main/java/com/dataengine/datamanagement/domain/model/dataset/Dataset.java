package com.dataengine.datamanagement.domain.model.dataset;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.dataengine.common.domain.model.base.BaseEntity;
import com.dataengine.datamanagement.common.enums.DatasetStatusType;
import com.dataengine.datamanagement.common.enums.DatasetType;
import lombok.Getter;
import lombok.Setter;

import java.io.File;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * 数据集实体（与数据库表 t_dm_datasets 对齐）
 */
@Getter
@Setter
@TableName(value = "t_dm_datasets", autoResultMap = true)
public class Dataset extends BaseEntity<String> {
    /**
     * 数据集名称
     */
    private String name;
    /**
     * 数据集描述
     */
    private String description;
    /**
     * 数据集类型
     */
    private DatasetType datasetType;
    /**
     * 数据集分类
     */
    private String category;
    /**
     * 数据集路径
     */
    private String path;
    /**
     * 数据集格式
     */
    private String format;
    /**
     * 数据集模式信息，JSON格式, 用于解析当前数据集的文件结构
     */
    private String schemaInfo;
    /**
     * 数据集大小（字节）
     */
    private Long sizeBytes = 0L;
    /**
     * 文件数量
     */
    private Long fileCount = 0L;
    /**
     * 记录数量
     */
    private Long recordCount = 0L;
    /**
     * 数据集保留天数
     */
    private Integer retentionDays = 0;
    /**
     * 额外元数据，JSON格式
     */
    private String metadata;
    /**
     * 数据集状态
     */
    private DatasetStatusType status;
    /**
     * 是否为公共数据集
     */
    private Boolean isPublic = false;
    /**
     * 是否为精选数据集
     */
    private Boolean isFeatured = false;
    /**
     * 数据集版本号
     */
    private Long version = 0L;

    // 聚合内的便捷集合（非持久化关联，由应用服务填充）
    @TableField(exist = false)
    private List<Tag> tags = new ArrayList<>();
    @TableField(exist = false)
    private List<DatasetFile> files = new ArrayList<>();

    public Dataset() {
    }

    public Dataset(String name, String description, DatasetType datasetType, String category, String path,
                   String format, DatasetStatusType status, String createdBy) {
        this.name = name;
        this.description = description;
        this.datasetType = datasetType;
        this.category = category;
        this.path = path;
        this.format = format;
        this.status = status;
        this.createdBy = createdBy;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public void initCreateParam(String datasetBasePath) {
        this.id = UUID.randomUUID().toString();
        this.path = datasetBasePath + File.separator + this.id;
        this.status = DatasetStatusType.DRAFT;
        this.createdBy = "system";
        this.updatedBy = "system";
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public void updateBasicInfo(String name, String description, String category) {
        if (name != null && !name.isEmpty()) this.name = name;
        if (description != null) this.description = description;
        if (category != null) this.category = category;
        this.updatedAt = LocalDateTime.now();
    }

    public void updateStatus(DatasetStatusType status, String updatedBy) {
        this.status = status;
        this.updatedBy = updatedBy;
        this.updatedAt = LocalDateTime.now();
    }

    public void addFile(DatasetFile file) {
        this.files.add(file);
        this.fileCount = this.fileCount + 1;
        this.sizeBytes = this.sizeBytes + (file.getFileSize() != null ? file.getFileSize() : 0L);
        this.updatedAt = LocalDateTime.now();
    }

    public void removeFile(DatasetFile file) {
        if (this.files.remove(file)) {
            this.fileCount = Math.max(0, this.fileCount - 1);
            this.sizeBytes = Math.max(0, this.sizeBytes - (file.getFileSize() != null ? file.getFileSize() : 0L));
            this.updatedAt = LocalDateTime.now();
        }
    }
}
