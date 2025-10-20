import { Select, Input, Form, Radio } from "antd";
import { dataSourceOptions } from "../../dataset.const";
import { DataSource } from "../../dataset.model";
import { useEffect, useState } from "react";
import { queryTasksUsingGet } from "@/pages/DataCollection/collection.apis";

export default function ImportConfiguration({ data, importFileRender }) {
  const [collectionOptions, setCollectionOptions] = useState([]);

  // 获取归集任务列表
  const fetchCollectionTasks = async () => {
    try {
      const data = await queryTasksUsingGet({ page: 0, size: 100 });
      const options = data.content.map((task: any) => ({
        label: task.name,
        value: task.id,
      }));
      setCollectionOptions(options);
    } catch (error) {
      console.error("Error fetching collection tasks:", error);
    }
  };

  useEffect(() => {
    fetchCollectionTasks();
  }, []);

  return (
    <>
      <div className="space-y-4 pt-4">
        <h2 className="font-medium text-gray-900 mt-4 text-base">
          数据导入配置
        </h2>
        <Form.Item
          label="数据源"
          name={["config", "source"]}
          rules={[{ required: true, message: "请选择数据源" }]}
        >
          <Radio.Group
            buttonStyle="solid"
            options={dataSourceOptions}
            optionType="button"
          />
        </Form.Item>
        <Form.Item
          label="目标位置"
          name={["config", "target"]}
          rules={[{ required: true, message: "请选择目标位置" }]}
        >
          <Select
            className="w-full"
            options={[
              { label: "本地文件夹", value: DataSource.UPLOAD },
              { label: "数据库", value: DataSource.DATABASE },
            ]}
            disabled
          ></Select>
        </Form.Item>
        {data?.config?.source === DataSource.COLLECTION && (
          <Form.Item
            name={["config", "collectionId"]}
            label="归集任务"
            required
          >
            <Select placeholder="请选择归集任务" options={collectionOptions} />
          </Form.Item>
        )}

        {/* nas import */}
        {data?.config?.source === DataSource.NAS && (
          <div className="grid grid-cols-2 gap-3 p-4 bg-blue-50 rounded-lg">
            <Form.Item
              name={["config", "nasPath"]}
              rules={[{ required: true }]}
              label="NAS地址"
            >
              <Input placeholder="192.168.1.100" />
            </Form.Item>
            <Form.Item
              name={["config", "sharePath"]}
              rules={[{ required: true }]}
              label="共享路径"
            >
              <Input placeholder="/share/data" />
            </Form.Item>
            <Form.Item
              name={["config", "sharePath"]}
              rules={[{ required: true }]}
              label="用户名"
            >
              <Input placeholder="用户名" />
            </Form.Item>
            <Form.Item
              name={["config", "password"]}
              rules={[{ required: true }]}
              label="密码"
            >
              <Input type="password" placeholder="密码" />
            </Form.Item>
          </div>
        )}
        {/* obs import */}
        {data?.config?.source === DataSource.OBS && (
          <div className="grid grid-cols-2 gap-3 p-4 bg-blue-50 rounded-lg">
            <Form.Item
              name={["config", "endpoint"]}
              rules={[{ required: true }]}
              label="Endpoint"
            >
              <Input
                className="h-8 text-xs"
                placeholder="obs.cn-north-4.myhuaweicloud.com"
              />
            </Form.Item>
            <Form.Item
              name={["config", "bucket"]}
              rules={[{ required: true }]}
              label="Bucket"
            >
              <Input className="h-8 text-xs" placeholder="my-bucket" />
            </Form.Item>
            <Form.Item
              name={["config", "accessKey"]}
              rules={[{ required: true }]}
              label="Access Key"
            >
              <Input className="h-8 text-xs" placeholder="Access Key" />
            </Form.Item>
            <Form.Item
              name={["config", "secretKey"]}
              rules={[{ required: true }]}
              label="Secret Key"
            >
              <Input
                type="password"
                className="h-8 text-xs"
                placeholder="Secret Key"
              />
            </Form.Item>
          </div>
        )}

        {/* Local Upload Component */}
        {data?.config?.source === DataSource.UPLOAD && (
          <Form.Item
            label="上传文件"
            name="files"
            rules={[
              {
                required: true,
                message: "请上传文件",
              },
            ]}
          >
            {importFileRender()}
          </Form.Item>
        )}

        {/* Target Configuration */}
        {data?.config?.target && data?.config?.target !== DataSource.UPLOAD && (
          <div className="space-y-3 p-4 bg-blue-50 rounded-lg">
            {data?.config?.target === DataSource.DATABASE && (
              <div className="grid grid-cols-2 gap-3">
                <Form.Item
                  name={["config", "databaseType"]}
                  rules={[{ required: true }]}
                  label="数据库类型"
                >
                  <Select
                    className="w-full"
                    options={[
                      { label: "MySQL", value: "mysql" },
                      { label: "PostgreSQL", value: "postgresql" },
                      { label: "MongoDB", value: "mongodb" },
                    ]}
                  ></Select>
                </Form.Item>
                <Form.Item
                  name={["config", "tableName"]}
                  rules={[{ required: true }]}
                  label="表名"
                >
                  <Input className="h-8 text-xs" placeholder="dataset_table" />
                </Form.Item>
                <Form.Item
                  name={["config", "connectionString"]}
                  rules={[{ required: true }]}
                  label="连接字符串"
                >
                  <Input
                    className="h-8 text-xs col-span-2"
                    placeholder="数据库连接字符串"
                  />
                </Form.Item>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}
