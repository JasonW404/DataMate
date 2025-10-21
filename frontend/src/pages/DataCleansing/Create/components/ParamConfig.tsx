import React from "react";
import {
  Input,
  Select,
  Radio,
  Checkbox,
  Form,
  InputNumber,
  Slider,
  Space,
} from "antd";
import { ConfigI, OperatorI } from "@/pages/OperatorMarket/operator.model";

interface ParamConfigProps {
  operator: OperatorI;
  paramKey: string;
  param: ConfigI;
  onParamChange?: (operatorId: string, paramKey: string, value: any) => void;
}

const ParamConfig: React.FC<ParamConfigProps> = ({
  operator,
  paramKey,
  param,
  onParamChange,
}) => {
  if (!param) return null;
  const [value, setValue] = React.useState(param.value || param.defaultVal);
  const updateValue = (newValue: any) => {
    setValue(newValue);
    return onParamChange && onParamChange(operator.id, paramKey, newValue);
  };

  switch (param.type) {
    case "input":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Input
            value={value}
            onChange={(e) => updateValue(e.target.value)}
            placeholder={`请输入${param.name}`}
            className="w-full"
          />
        </Form.Item>
      );
    case "select":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Select
            value={value}
            onChange={updateValue}
            options={(param.options || []).map((option: any) =>
              typeof option === "string"
                ? { label: option, value: option }
                : option
            )}
            placeholder={`请选择${param.name}`}
            className="w-full"
          />
        </Form.Item>
      );
    case "radio":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Radio.Group
            value={value}
            onChange={(e) => updateValue(e.target.value)}
          >
            {(param.options || []).map((option: any) => (
              <Radio
                key={typeof option === "string" ? option : option.value}
                value={typeof option === "string" ? option : option.value}
              >
                {typeof option === "string" ? option : option.label}
              </Radio>
            ))}
          </Radio.Group>
        </Form.Item>
      );
    case "checkbox":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Checkbox.Group
            value={value}
            onChange={updateValue}
            options={param.options || []}
          />
        </Form.Item>
      );
    case "slider":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <div className="flex items-center gap-1">
            <Slider
              value={value}
              onChange={updateValue}
              tooltip={{ open: true }}
              marks={{
                [param.min || 0]: `${param.min || 0}`,
                [param.min + (param.max - param.min) / 2]: `${
                  (param.min + param.max) / 2
                }`,
                [param.max || 100]: `${param.max || 100}`,
              }}
              min={param.min || 0}
              max={param.max || 100}
              step={param.step || 1}
              className="flex-1"
            />
            <InputNumber
              min={param.min || 0}
              max={param.max || 100}
              step={param.step || 1}
              value={value}
              onChange={updateValue}
              style={{ width: 80 }}
            />
          </div>
        </Form.Item>
      );
    case "range": {
      const min = param.min || 0;
      const max = param.max || 100;
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Slider
            value={Array.isArray(value) ? value : [value, value]}
            onChange={(val) =>
              updateValue(Array.isArray(val) ? val : [val, val])
            }
            range
            min={min}
            max={max}
            step={param.step || 1}
            className="w-full"
          />
          <Space>
            <InputNumber
              min={min}
              max={max}
              value={value[0]}
              onChange={(val1) => updateValue([val1, value[1]])}
              changeOnWheel
            />
            ~
            <InputNumber
              min={min}
              max={max}
              value={value[1]}
              onChange={(val2) => updateValue([value[0], val2])}
              changeOnWheel
            />
          </Space>
        </Form.Item>
      );
    }
    case "inputNumber":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <InputNumber
            value={value}
            onChange={(val) => updateValue(val)}
            placeholder={`请输入${param.name}`}
            className="w-full"
            min={param.min}
            max={param.max}
            step={param.step || 1}
          />
        </Form.Item>
      );

    case "switch":
      return (
        <Form.Item
          label={param.name}
          tooltip={param.description}
          key={paramKey}
        >
          <Checkbox
            checked={value as boolean}
            onChange={(e) => updateValue(e.target.checked)}
          >
            {param.name}
          </Checkbox>
        </Form.Item>
      );
    case "multiple":
      return (
        <div className="pl-4 border-l border-gray-300">
          {param.properties.map((subParam) => (
            <Config
              key={subParam.key}
              operator={operator}
              paramKey={subParam.key}
              param={subParam}
              onParamChange={onParamChange}
            />
          ))}
        </div>
      );
    default:
      return null;
  }
};

export default ParamConfig;
