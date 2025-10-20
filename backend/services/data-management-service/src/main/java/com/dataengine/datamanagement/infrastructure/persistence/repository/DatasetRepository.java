package com.dataengine.datamanagement.infrastructure.persistence.repository;

import com.baomidou.mybatisplus.extension.repository.IRepository;
import com.dataengine.datamanagement.domain.model.dataset.Dataset;
import com.dataengine.datamanagement.interfaces.dto.AllDatasetStatisticsResponse;
import org.apache.ibatis.session.RowBounds;

import java.util.List;


/**
 * 数据集仓储层
 *
 * @author dallas
 * @since 2025-10-15
 */
public interface DatasetRepository extends IRepository<Dataset> {
    Dataset findByName(String name);

    List<Dataset> findByCriteria(String type, String status, String keyword, List<String> tagList, RowBounds bounds);

    long countByCriteria(String type, String status, String keyword, List<String> tagList);

    AllDatasetStatisticsResponse getAllDatasetStatistics();
}
