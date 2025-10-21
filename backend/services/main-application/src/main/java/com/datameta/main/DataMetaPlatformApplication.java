package com.datameta.main;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * 数据引擎平台主应用
 * 聚合所有业务服务JAR包的微服务启动类
 *
 * @author Data Meta Team
 * @version 1.0.0
 */
@SpringBootApplication
@ComponentScan(basePackages = {
        "com.datameta.main",
        "com.datameta.datamanagement",
        "com.datameta.collection",
        "com.datameta.operator",
        "com.datameta.cleaning",
        "com.datameta.synthesis",
        "com.datameta.annotation",
        "com.datameta.evaluation",
        "com.datameta.pipeline",
        "com.datameta.execution",
        "com.datameta.rag",
        "com.datameta.shared",
        "com.datameta.common"
})
@MapperScan(basePackages = {
        "com.datameta.collection.infrastructure.persistence.mapper",
        "com.datameta.datamanagement.infrastructure.persistence.mapper",
        "com.datameta.operator.infrastructure.persistence.mapper",
        "com.datameta.cleaning.infrastructure.persistence.mapper",
        "com.datameta.common.infrastructure.mapper"
})
@EnableTransactionManagement
@EnableAsync
@EnableScheduling
public class DataMetaPlatformApplication {

    public static void main(String[] args) {
        SpringApplication.run(DataMetaPlatformApplication.class, args);
    }
}
