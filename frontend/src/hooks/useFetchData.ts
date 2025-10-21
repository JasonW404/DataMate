// 首页数据获取
import { useState } from "react";
import { useDebouncedEffect } from "./useDebouncedEffect";
import Loading from "@/utils/loading";
import { App } from "antd";

export default function useFetchData<T>(
  fetchFunc: (params?: any) => Promise<any>,
  mapDataFunc: (data: any) => T = (data) => data as T
) {
  const { message } = App.useApp();
  // 表格数据
  const [tableData, setTableData] = useState<T[]>([]);
  // 设置加载状态
  const [loading, setLoading] = useState(false);

  // 搜索参数
  const [searchParams, setSearchParams] = useState({
    keyword: "",
    filter: {
      type: [] as string[],
      status: [] as string[],
      tags: [] as string[],
    },
    current: 1,
    pageSize: 12,
  });

  // 分页配置
  const [pagination, setPagination] = useState({
    total: 0,
    showSizeChanger: true,
    pageSizeOptions: ["12", "24", "48"],
    showTotal: (total: number) => `共 ${total} 条`,
    onChange: (current: number, pageSize?: number) => {
      setSearchParams((prev) => ({
        ...prev,
        current,
        pageSize: pageSize || prev.pageSize,
      }));
    },
  });

  const handleFiltersChange = (searchFilters: { [key: string]: string[] }) => {
    setSearchParams({
      ...searchParams,
      current: 1,
      filter: { ...searchParams.filter, ...searchFilters },
    });
  };

  function getFirstOfArray(arr: string[]) {
    if (!arr || arr.length === 0 || !Array.isArray(arr)) return undefined;
    if (arr[0] === "all") return undefined;
    return arr[0];
  }

  async function fetchData(extraParams = {}) {
    const { keyword, filter, current, pageSize } = searchParams;
    Loading.show();
    setLoading(true);
    try {
      const { data } = await fetchFunc({
        ...filter,
        ...extraParams,
        keyword,
        type: getFirstOfArray(filter?.type) || undefined,
        status: getFirstOfArray(filter?.status) || undefined,
        tags: filter?.tags?.length ? filter.tags.join(",") : undefined,
        page: current - 1,
        size: pageSize,
      });
      setPagination((prev) => ({
        ...prev,
        total: data?.totalElements || 0,
      }));
      let result = [];
      if (mapDataFunc) {
        result = data?.content.map(mapDataFunc) ?? [];
      }
      setTableData(result);
    } catch (error) {
      console.error(error)
      message.error("数据获取失败，请稍后重试");
    } finally {
      Loading.hide();
      setLoading(false);
    }
  }

  useDebouncedEffect(
    () => {
      fetchData();
    },
    [searchParams],
    searchParams?.keyword ? 500 : 0
  );

  return {
    loading,
    tableData,
    pagination: {
      ...pagination,
      current: searchParams.current,
      pageSize: searchParams.pageSize,
    },
    searchParams,
    setSearchParams,
    setPagination,
    handleFiltersChange,
    fetchData,
  };
}
