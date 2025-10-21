package com.datameta.cleaning.infrastructure.persistence.mapper;

import com.datameta.cleaning.domain.model.TemplateWithInstance;
import com.datameta.cleaning.interfaces.dto.CleaningTemplate;
import com.datameta.cleaning.interfaces.dto.OperatorResponse;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface CleaningTemplateMapper {

    List<TemplateWithInstance> findAllTemplates(@Param("keywords") String keywords);

    List<OperatorResponse> findAllOperators();

    CleaningTemplate findTemplateById(@Param("templateId") String templateId);

    void insertTemplate(CleaningTemplate template);

    void updateTemplate(CleaningTemplate template);

    void deleteTemplate(@Param("templateId") String templateId);
}
