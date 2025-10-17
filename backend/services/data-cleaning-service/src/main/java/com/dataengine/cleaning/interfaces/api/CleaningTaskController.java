package com.dataengine.cleaning.interfaces.api;

import com.dataengine.cleaning.interfaces.dto.CleaningTask;
import com.dataengine.cleaning.interfaces.dto.CreateCleaningTaskRequest;
import com.dataengine.cleaning.application.service.CleaningTaskService;

import com.dataengine.common.interfaces.PagedResponse;
import com.dataengine.common.interfaces.Response;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@RestController
@RequestMapping("/cleaning/tasks")
@RequiredArgsConstructor
public class CleaningTaskController {
    private final CleaningTaskService cleaningTaskService;

    @GetMapping
    public ResponseEntity<Response<PagedResponse<CleaningTask>>> cleaningTasksGet(
            @RequestParam("page") Integer page,
            @RequestParam("size") Integer size, @RequestParam(value = "status", required = false) String status,
            @RequestParam(value = "keywords", required = false) String keywords) {
        List<CleaningTask> tasks = cleaningTaskService.getTasks(status, keywords, page, size);
        int count = cleaningTaskService.countTasks(status, keywords);
        int totalPages = (count + size + 1) / size;
        return ResponseEntity.ok(Response.ok(PagedResponse.of(tasks, page, count, totalPages)));
    }

    @PostMapping
    public ResponseEntity<Response<CleaningTask>> cleaningTasksPost(@RequestBody CreateCleaningTaskRequest request) {
        return ResponseEntity.ok(Response.ok(cleaningTaskService.createTask(request)));
    }

    @PostMapping("/{taskId}/stop")
    public ResponseEntity<Response<Object>> cleaningTasksStop(@PathVariable("taskId") String taskId) {
        cleaningTaskService.stopTask(taskId);
        return ResponseEntity.ok(Response.ok(null));
    }

    @PostMapping("/{taskId}/execute")
    public ResponseEntity<Response<Object>> cleaningTasksStart(@PathVariable("taskId") String taskId) {
        cleaningTaskService.executeTask(taskId);
        return ResponseEntity.ok(Response.ok(null));
    }

    @GetMapping("/{taskId}")
    public ResponseEntity<Response<CleaningTask>> cleaningTasksTaskIdGet(@PathVariable("taskId") String taskId) {
        return ResponseEntity.ok(Response.ok(cleaningTaskService.getTask(taskId)));
    }

    @DeleteMapping("/{taskId}")
    public ResponseEntity<Response<Object>> cleaningTasksTaskIdDelete(@PathVariable("taskId") String taskId) {
        cleaningTaskService.deleteTask(taskId);
        return ResponseEntity.ok(Response.ok(null));
    }
}
