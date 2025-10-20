import { useState } from "react";

import { ArrowLeft } from "lucide-react";
import { Button, Form, App } from "antd";
import { Link, useNavigate } from "react-router";
import { createDatasetUsingPost } from "../dataset.api";
import { DatasetType, DataSource } from "../dataset.model";
import BasicInformation from "./components/BasicInformation";
import ImportConfiguration from "./components/ImportConfiguration";
import { useImportFile } from "../hooks";

export default function DatasetCreate() {
  const navigate = useNavigate();
  const { message } = App.useApp();
  const [form] = Form.useForm();
  const { importFileRender, handleUpload } = useImportFile();

  const [newDataset, setNewDataset] = useState({
    name: "",
    description: "",
    datasetType: DatasetType.TEXT,
    tags: [],
    config: {
      source: DataSource.UPLOAD,
      target: DataSource.UPLOAD,
      nasHost: "",
      sharePath: "",
      username: "",
      password: "",
      endpoint: "",
      bucket: "",
      accessKey: "",
      secretKey: "",
      databaseType: "",
      databaseName: "",
      tableName: "",
      dbType: "",
      connectionString: "",
    },
  });

  const handleSubmit = async () => {
    const formValues = await form.validateFields();

    const params = {
      ...formValues,
      files: undefined,
    };
    let dataset;
    try {
      const { data } = await createDatasetUsingPost(params);
      dataset = data;
      if (formValues?.config?.source === DataSource.UPLOAD) {
        handleUpload(dataset);
      }
      message.success(`数据集创建成功`);
      navigate("/data/management");
    } catch (error) {
      console.error(error);
      message.error("数据集创建失败，请重试");
      return;
    }
  };

  const handleValuesChange = (_, allValues) => {
    setNewDataset({ ...newDataset, ...allValues });
  };

  return (
    <div className="h-full flex flex-col flex-1">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          <Link to="/data/management">
            <Button type="text">
              <ArrowLeft className="w-4 h-4 mr-1" />
            </Button>
          </Link>
          <h1 className="text-xl font-bold bg-clip-text">创建数据集</h1>
        </div>
      </div>

      {/* form */}
      <div className="h-full flex flex-col flex-1 overflow-auto bg-white border-gray-200 rounded shadow-sm">
        <div className="flex-1 p-6 overflow-auto">
          <Form
            form={form}
            initialValues={newDataset}
            onValuesChange={handleValuesChange}
            layout="vertical"
          >
            <BasicInformation data={newDataset} setData={setNewDataset} />

            {/* Import Configuration */}
            <ImportConfiguration
              data={newDataset}
              importFileRender={importFileRender}
            />
          </Form>
        </div>
        <div className="flex gap-2 justify-end p-6 border-t border-gray-200">
          <Button onClick={() => navigate("/dataset-management")}>取消</Button>
          <Button type="primary" onClick={handleSubmit}>
            确定
          </Button>
        </div>
      </div>
    </div>
  );
}
