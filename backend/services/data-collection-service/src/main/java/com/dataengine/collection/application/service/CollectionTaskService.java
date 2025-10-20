package com.dataengine.collection.application.service;

import com.dataengine.collection.domain.model.CollectionTask;
import com.dataengine.collection.domain.model.TaskExecution;
import com.dataengine.collection.domain.model.TaskStatus;
import com.dataengine.collection.domain.model.DataxTemplate;
import com.dataengine.collection.infrastructure.persistence.mapper.CollectionTaskMapper;
import com.dataengine.collection.infrastructure.persistence.mapper.TaskExecutionMapper;
import com.dataengine.collection.interfaces.dto.SyncMode;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class CollectionTaskService {
    private final CollectionTaskMapper taskMapper;
    private final TaskExecutionMapper executionMapper;
    private final DataxExecutionService dataxExecutionService;

    @Transactional
    public CollectionTask create(CollectionTask task) {
        task.setStatus(TaskStatus.READY);
        task.setCreatedAt(LocalDateTime.now());
        task.setUpdatedAt(LocalDateTime.now());
        taskMapper.insert(task);
        if (Objects.equals(task.getSyncMode(), SyncMode.ONCE.getValue())) {
            TaskExecution exec = dataxExecutionService.createExecution(task);
            int timeout = task.getTimeoutSeconds() == null ? 3600 : task.getTimeoutSeconds();
            dataxExecutionService.runAsync(task, exec.getId(), timeout);
            log.info("Triggered DataX execution for task {} at {}, execId={}", task.getId(), LocalDateTime.now(), exec.getId());
        }
        return task;
    }

    @Transactional
    public CollectionTask update(CollectionTask task) {
        task.setUpdatedAt(LocalDateTime.now());
        taskMapper.update(task);
        return task;
    }

    @Transactional
    public void delete(String id) { taskMapper.deleteById(id); }

    public CollectionTask get(String id) { return taskMapper.selectById(id); }

    public List<CollectionTask> list(Integer page, Integer size, String status, String name) {
        Map<String, Object> p = new HashMap<>();
        p.put("status", status);
        p.put("name", name);
        if (page != null && size != null) {
            p.put("offset", page * size);
            p.put("limit", size);
        }
        return taskMapper.selectAll(p);
    }

    @Transactional
    public TaskExecution startExecution(CollectionTask task) {
        TaskExecution exec = new TaskExecution();
        exec.setId(UUID.randomUUID().toString());
        exec.setTaskId(task.getId());
        exec.setTaskName(task.getName());
        exec.setStatus(TaskStatus.RUNNING);
        exec.setProgress(0.0);
        exec.setStartedAt(LocalDateTime.now());
        exec.setCreatedAt(LocalDateTime.now());
        executionMapper.insert(exec);
        taskMapper.updateLastExecution(task.getId(), exec.getId());
        taskMapper.updateStatus(task.getId(), TaskStatus.RUNNING.name());
        return exec;
    }

    // ---- Template related merged methods ----
    public List<DataxTemplate> listTemplates(String sourceType, String targetType, int page, int size) {
        int offset = page * size;
        return taskMapper.selectList(sourceType, targetType, offset, size);
    }

    public int countTemplates(String sourceType, String targetType) {
        return taskMapper.countTemplates(sourceType, targetType);
    }
}
