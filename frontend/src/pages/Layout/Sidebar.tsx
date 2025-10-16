import React, { memo, useEffect, useState } from "react";
import { Button, Menu } from "antd";
import {
  CloseOutlined,
  MenuOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import { ClipboardList, Sparkles } from "lucide-react";
import { antMenuItems, antMenuItems as items } from "@/pages/Layout/menu";
import { NavLink, useLocation, useNavigate } from "react-router";
import TaskUpload from "./TaskUpload";

const TaskUploadPopover = ({ sidebarOpen, toggleShowTaskPopover }) => {
  const arrowStyle = sidebarOpen ? {} : { top: "calc(100% - 68px)" };
  const popoverStyle = sidebarOpen
    ? {
        bottom: "48px",
        left: "0px",
      }
    : {
        bottom: "-48px",
        left: "68px",
      };

  return (
    <div
      id="header-task-popover"
      className={`absolute left-full w-md transition-all duration-300 ease-in-out z-50 opacity-0 invisible transform -translate-x-4`}
      style={popoverStyle}
    >
      {/* 箭头 - 指向按钮中心 */}
      {/* <div
        className="absolute -left-2 w-0 h-0 transform -translate-y-1/2"
        style={{
          borderTop: "8px solid transparent",
          borderBottom: "8px solid transparent",
          borderRight: "8px solid #e5e7eb",
          ...arrowStyle,
        }}
      />
      <div
        className="absolute -left-1.5 top-1/2 w-0 h-0 transform -translate-y-1/2"
        style={{
          borderTop: "8px solid transparent",
          borderBottom: "8px solid transparent",
          borderRight: "8px solid white",
          ...arrowStyle,
        }}
      /> */}
      <div className="bg-white rounded-lg shadow-lg border border-gray-200 min-w-80">
        <div className="flex justify-between items-center p-3 border-b border-gray-100">
          <span className="text-sm font-medium text-gray-900">任务中心</span>
          <Button
            type="text"
            size="small"
            icon={<CloseOutlined />}
            onClick={() => toggleShowTaskPopover(false)}
          />
        </div>
        <div className="p-0 h-[250px] overflow-y-auto">
          <TaskUpload />
        </div>
      </div>
    </div>
  );
};

const AsiderAndHeaderLayout = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [activeItem, setActiveItem] = useState<string>("management");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [taskCenterVisible, setTaskCenterVisible] = useState(false);

  // Initialize active item based on current pathname
  const initActiveItem = () => {
    for (let index = 0; index < antMenuItems.length; index++) {
      const element = antMenuItems[index];
      if (element.children) {
        element.children.forEach((subItem) => {
          if (pathname.includes(subItem.key)) {
            setActiveItem(subItem.key);
            return;
          }
        });
      } else if (pathname.includes(element.key)) {
        setActiveItem(element.key);
        return;
      }
    }
  };

  useEffect(() => {
    initActiveItem();
  }, [pathname]);

  const toggleShowTaskPopover = (show: boolean = true) => {
    const taskEl = document.getElementById("header-task-popover");
    if (show && !taskEl?.classList.contains("show-task-popover")) {
      taskEl?.classList?.add("show-task-popover");
      return;
    }
    if (!show && taskEl?.classList.contains("show-task-popover")) {
      taskEl?.classList?.remove("show-task-popover");
    }
  };

  return (
    <div
      className={`${
        sidebarOpen ? "w-64" : "w-20"
      } bg-white border-r border-gray-200 transition-all duration-300 flex flex-col relative`}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {sidebarOpen && (
          <NavLink to="/" className="flex items-center gap-2 cursor-pointer">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold text-gray-900">ModelEngine</span>
          </NavLink>
        )}
        <span
          className="cursor-pointer hover:text-blue-500"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? <CloseOutlined /> : <MenuOutlined className="ml-4" />}
        </span>
      </div>

      {/* Navigation */}
      <div className="flex-1">
        <Menu
          mode="inline"
          inlineCollapsed={!sidebarOpen}
          items={items}
          selectedKeys={[activeItem]}
          defaultOpenKeys={["synthesis"]}
          onClick={({ key }) => {
            setActiveItem(key);
            console.log(`/data/${key}`);
            navigate(`/data/${key}`);
          }}
        />
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        {sidebarOpen ? (
          <div className="space-y-2">
            <div className="relative">
              <Button block onClick={() => toggleShowTaskPopover(true)}>
                任务中心
              </Button>
              <TaskUploadPopover
                sidebarOpen={sidebarOpen}
                toggleShowTaskPopover={toggleShowTaskPopover}
              />
            </div>
            <Button block onClick={() => navigate("/data/settings")}>
              设置
            </Button>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="relative">
              <Button
                block
                onClick={() => toggleShowTaskPopover(true)}
                icon={<ClipboardList className="w-4 h-4" />}
              ></Button>
              <TaskUploadPopover
                sidebarOpen={sidebarOpen}
                toggleShowTaskPopover={toggleShowTaskPopover}
              />
            </div>
            <Button block onClick={() => navigate("/data/settings")}>
              <SettingOutlined />
            </Button>
          </div>
        )}
      </div>

      {/* 添加遮罩层，点击外部区域时关闭 */}
      {taskCenterVisible && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            console.log('clicked outside');
            
            setTaskCenterVisible(false);
            toggleShowTaskPopover(false);
          }}
        />
      )}
    </div>
  );
};

export default memo(AsiderAndHeaderLayout);
