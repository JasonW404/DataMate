package com.dataengine.datamanagement.domain.model.dataset;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
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
public class Dataset {
    @TableId
    private String id;
    private String name;
    private String description;
    // DB: dataset_type
    private String datasetType;

    private String category;

    // DB: path
    private String path;
    // DB: format
    private String format;
    private String schemaInfo;

    // DB: size_bytes
    private Long sizeBytes = 0L;
    private Long fileCount = 0L;
    private Long recordCount = 0L;
    private Integer retentionDays = 0;

    private String metadata;

    private String status; // DRAFT/ACTIVE/ARCHIVED/PROCESSING
    private Boolean isPublic = false;
    private Boolean isFeatured = false;
    private Long version = 0L;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String createdBy;
    private String updatedBy;

    // 聚合内的便捷集合（非持久化关联，由应用服务填充）
    @TableField(exist = false)
    private List<Tag> tags = new ArrayList<>();
    @TableField(exist = false)
    private List<DatasetFile> files = new ArrayList<>();

    public Dataset() {
    }

    public Dataset(String name, String description, String datasetType, String category, String path, String format,
                   String status, String createdBy) {
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
        this.status = StatusConstants.DatasetStatuses.ACTIVE;
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

    public void updateStatus(String status, String updatedBy) {
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
