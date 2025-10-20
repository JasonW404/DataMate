package com.dataengine.operator.infrastructure.persistence.mapper;

import com.dataengine.operator.domain.modal.RelationCategoryDTO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface CategoryRelationMapper {

    List<RelationCategoryDTO> findAllRelationWithCategory();

    List<RelationCategoryDTO> findFullOuterJoinNative();

    void batchInsert(@Param("operatorId") String operatorId, @Param("categories") List<Integer> categories);
}
