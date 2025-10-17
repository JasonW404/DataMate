package com.dataengine.cleaning.interfaces.api;

import com.dataengine.cleaning.application.service.CleaningTemplateService;
import com.dataengine.cleaning.interfaces.dto.CleaningTemplate;
import com.dataengine.cleaning.interfaces.dto.CreateCleaningTemplateRequest;
import com.dataengine.cleaning.interfaces.dto.UpdateCleaningTemplateRequest;
import com.dataengine.common.infrastructure.common.Response;
import com.dataengine.common.interfaces.PagedResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/cleaning/templates")
@RequiredArgsConstructor
public class CleaningTemplateController {
    private final CleaningTemplateService cleaningTemplateService;

    @GetMapping
    public ResponseEntity<Response<PagedResponse<CleaningTemplate>>> cleaningTemplatesGet() {
        return ResponseEntity.ok(Response.ok(PagedResponse.of(cleaningTemplateService.getTemplates())));
    }

    @PostMapping
    public ResponseEntity<Response<CleaningTemplate>> cleaningTemplatesPost(
            @RequestBody CreateCleaningTemplateRequest request) {
        return ResponseEntity.ok(Response.ok(cleaningTemplateService.createTemplate(request)));
    }

    @GetMapping("/{templateId}")
    public ResponseEntity<Response<CleaningTemplate>> cleaningTemplatesTemplateIdGet(
            @PathVariable("templateId") String templateId) {
        return ResponseEntity.ok(Response.ok(cleaningTemplateService.getTemplate(templateId)));
    }

    @PutMapping("/{templateId}")
    public ResponseEntity<Response<CleaningTemplate>> cleaningTemplatesTemplateIdPut(
            @PathVariable("templateId") String templateId, @RequestBody UpdateCleaningTemplateRequest request) {
        return ResponseEntity.ok(Response.ok(cleaningTemplateService.updateTemplate(templateId, request)));
    }

    @DeleteMapping("/{templateId}")
    public ResponseEntity<Response<Object>> cleaningTemplatesTemplateIdDelete(
            @PathVariable("templateId") String templateId) {
        cleaningTemplateService.deleteTemplate(templateId);
        return ResponseEntity.noContent().build();
    }
}
