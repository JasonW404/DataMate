import { useState } from "react";
import { Table, Progress, Badge, Button, Tooltip, Card } from "antd";
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  DatabaseOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import { SearchControls } from "@/components/SearchControls";
import CardView from "@/components/CardView";
import { useNavigate } from "react-router";
import { queryCleaningJobsUsingGet } from "../cleansing-apis";
import { TaskStatusMap, templateTypesMap } from "../cleansing-model";
import type { Dataset } from "@/types/dataset";
import { JobStatus } from "@/types/cleansing";
import useFetchData from "@/hooks/useFetchData";

export default function TaskList() {
  const navigate = useNavigate();
  const [viewMode, setViewMode] = useState<"card" | "list">("list");
  const filterOptions = [
    {
      key: "type",
      label: "类型",
      options: [
        { label: "所有类型", value: "all" },
        ...Object.values(templateTypesMap),
      ],
    },
    {
      key: "status",
      label: "状态",
      options: [
        { label: "所有状态", value: "all" },
        ...Object.values(TaskStatusMap),
      ],
    },
  ];

  const mapTask = (task) => ({
    ...task,
    icon: <DatabaseOutlined style={{ color: "#1677ff" }} />,
    iconColor: "bg-blue-100",
    status: TaskStatusMap[task.status],
    tags: task.rules.map((item) => item.name),
    statistics: [
      { label: "进度", value: `${task.progress}%` },
      { label: "已处理", value: task.statistics.processedRecords },
      { label: "总数", value: task.statistics.totalRecords },
    ],
    lastModified: task.startTime,
  });

  const {
    tableData,
    pagination,
    searchParams,
    setSearchParams,
    fetchData,
    handleFiltersChange,
  } = useFetchData(queryCleaningJobsUsingGet, mapTask);

  const handleViewTask = (task: any) => {
    navigate("/data/cleansing/task-detail/" + task.id);
  };

  const pauseTask = () => {};

  const startTask = () => {};

  const deleteTask = () => {};

  const taskOperations = (record) => {
    const isRunning = record.status.value === JobStatus.RUNNING;
    const isPending = record.status.value === JobStatus.PENDING;
    const pauseBtn = {
      key: "pause",
      label: "暂停",
      icon: isRunning ? <PauseCircleOutlined /> : <PlayCircleOutlined />,
      onClick: pauseTask, // implement pause/play logic
    };

    const startBtn = {
      key: "start",
      label: "启动",
      icon: isRunning ? <PauseCircleOutlined /> : <PlayCircleOutlined />,
      onClick: startTask, // implement pause/play logic
    };
    return [
      isRunning && pauseBtn,
      isPending && startBtn,
      {
        key: "delete",
        label: "删除",
        icon: <DeleteOutlined />,
        onClick: deleteTask, // implement delete logic
      },
    ];
  };

  const taskColumns = [
    {
      title: "任务名称",
      dataIndex: "name",
      key: "name",
      fixed: "left",
      render: (text: string, record: any) => (
        <a onClick={() => handleViewTask(record)}>{text}</a>
      ),
    },
    {
      title: "数据集",
      dataIndex: "dataset",
      key: "dataset",
      render: (dataset: Dataset) => {
        return (
          <Button
            type="link"
            onClick={() => navigate("/data/management/detail/" + dataset.id)}
          >
            {dataset.name}
          </Button>
        );
      },
    },
    {
      title: "状态",
      dataIndex: "status",
      key: "status",
      render: (status: any) => {
        return <Badge color={status.color} text={status.label} />;
      },
    },
    {
      title: "开始时间",
      dataIndex: "startTime",
      key: "startTime",
    },
    {
      title: "进度",
      dataIndex: "progress",
      key: "progress",
      width: 200,
      render: (progress: number) => (
        <Progress percent={progress} size="small" />
      ),
    },
    {
      title: "操作",
      key: "action",
      fixed: "right",
      render: (text: string, record: any) => (
        <div className="flex gap-2">
          {taskOperations(record).map((op) =>
            op ? (
              <Tooltip key={op.key} title={op.label}>
                <Button
                  type="text"
                  icon={op.icon}
                  onClick={() => op.onClick(record)}
                />
              </Tooltip>
            ) : null
          )}
        </div>
      ),
    },
  ];
  return (
    <>
      {/* Search and Filters */}
      <SearchControls
        className="mb-4"
        searchTerm={searchParams.keywords}
        onSearchChange={(keywords) =>
          setSearchParams({ ...searchParams, keywords })
        }
        searchPlaceholder="搜索任务名称、描述"
        filters={filterOptions}
        onFiltersChange={handleFiltersChange}
        viewMode={viewMode}
        onViewModeChange={setViewMode}
        showViewToggle={true}
        onReload={fetchData}
      />
      {/* Task List */}
      {viewMode === "card" ? (
        <CardView
          data={tableData}
          operations={taskOperations}
          onView={(item) =>
            handleViewTask(tableData.find((t) => t.id === item.id))
          }
          pagination={pagination}
        />
      ) : (
        <Card>
          <Table
            columns={taskColumns}
            dataSource={tableData}
            rowKey="id"
            scroll={{ x: "max-content", y: "calc(100vh - 20rem)" }}
            pagination={pagination}
          />
        </Card>
      )}
    </>
  );
}
