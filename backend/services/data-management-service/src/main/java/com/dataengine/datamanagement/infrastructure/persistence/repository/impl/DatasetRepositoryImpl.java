package com.dataengine.datamanagement.infrastructure.persistence.repository.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.repository.CrudRepository;
import com.dataengine.datamanagement.domain.model.dataset.Dataset;
import com.dataengine.datamanagement.infrastructure.persistence.mapper.DatasetMapper;
import com.dataengine.datamanagement.infrastructure.persistence.repository.DatasetRepository;
import com.dataengine.datamanagement.interfaces.dto.AllDatasetStatisticsResponse;
import lombok.RequiredArgsConstructor;
import org.apache.ibatis.session.RowBounds;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 数据集仓储层实现类
 *
 * @author dallas
 * @since 2025-10-15
 */
@Repository
@RequiredArgsConstructor
public class DatasetRepositoryImpl extends CrudRepository<DatasetMapper, Dataset> implements DatasetRepository {
    private final DatasetMapper datasetMapper;

    @Override
    public Dataset findByName(String name) {
        return datasetMapper.selectOne(new LambdaQueryWrapper<Dataset>().eq(Dataset::getName, name));
    }

    @Override
    public List<Dataset> findByCriteria(String type, String status, String keyword, List<String> tagList,
                                        RowBounds bounds) {
        return datasetMapper.findByCriteria(type, status, keyword, tagList, bounds);
    }

    @Override
    public long countByCriteria(String type, String status, String keyword, List<String> tagList) {
        return datasetMapper.countByCriteria(type, status, keyword, tagList);
    }

    @Override
    public AllDatasetStatisticsResponse getAllDatasetStatistics() {
        return datasetMapper.getAllDatasetStatistics();
    }
}
