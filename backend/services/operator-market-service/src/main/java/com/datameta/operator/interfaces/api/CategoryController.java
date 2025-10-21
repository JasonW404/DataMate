package com.datameta.operator.interfaces.api;

import com.datameta.common.infrastructure.common.Response;
import com.datameta.common.interfaces.PagedResponse;
import com.datameta.operator.application.CategoryService;
import com.datameta.operator.interfaces.dto.CategoryTreeResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@RestController
@RequestMapping("/categories")
@RequiredArgsConstructor
public class CategoryController {
    private final CategoryService categoryService;

    @GetMapping("/tree")
    public ResponseEntity<Response<PagedResponse<CategoryTreeResponse>>> categoryTreeGet() {
        List<CategoryTreeResponse> allCategories = categoryService.getAllCategories();
        return ResponseEntity.ok(Response.ok(PagedResponse.of(allCategories)));
    }
}
