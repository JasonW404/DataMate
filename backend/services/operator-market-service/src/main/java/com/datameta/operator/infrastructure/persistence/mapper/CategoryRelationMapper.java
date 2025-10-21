package com.datameta.operator.infrastructure.persistence.mapper;

import com.datameta.operator.domain.modal.CategoryRelation;
import com.datameta.operator.domain.modal.RelationCategoryDTO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface CategoryRelationMapper {

    List<RelationCategoryDTO> findAllRelationWithCategory();

    List<CategoryRelation> findAllRelation();

    void batchInsert(@Param("operatorId") String operatorId, @Param("categories") List<Integer> categories);
}
