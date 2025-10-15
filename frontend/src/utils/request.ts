import Loading from "./loading";

/**
 * 通用请求工具类
 */
class Request {
  constructor(baseURL = "") {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      "Content-Type": "application/json",
      Accept: "*/*",
    };
    // 请求拦截器列表
    this.requestInterceptors = [];
    // 响应拦截器列表
    this.responseInterceptors = [];
  }

  _count = 0;
  $interval;

  get count() {
    return this._count;
  }

  set count(value) {
    clearTimeout(this.$interval);
    if (value > 0) {
      Loading.show();
    }
    if (value <= 0) {
      this.$interval = setTimeout(() => {
        Loading.hide();
      }, 300);
    }
    this._count = value >= 0 ? value : 0;
  }

  /**
   * 添加请求拦截器
   */
  addRequestInterceptor(interceptor) {
    this.requestInterceptors.push(interceptor);
  }

  /**
   * 添加响应拦截器
   */
  addResponseInterceptor(interceptor) {
    this.responseInterceptors.push(interceptor);
  }

  /**
   * 执行请求拦截器
   */
  async executeRequestInterceptors(config) {
    let processedConfig = { ...config };

    for (const interceptor of this.requestInterceptors) {
      processedConfig = (await interceptor(processedConfig)) || processedConfig;
    }

    return processedConfig;
  }

  /**
   * 执行响应拦截器
   */
  async executeResponseInterceptors(response, config) {
    let processedResponse = response;

    for (const interceptor of this.responseInterceptors) {
      processedResponse =
        (await interceptor(processedResponse, config)) || processedResponse;
    }

    return processedResponse;
  }

  /**
   * 构建完整URL
   */
  buildURL(url, params) {
    const fullURL = this.baseURL + url;
    if (!params) return fullURL;

    const searchParams = new URLSearchParams();
    Object.keys(params).forEach((key) => {
      if (params[key] !== undefined && params[key] !== null) {
        searchParams.append(key, params[key]);
      }
    });

    const queryString = searchParams.toString();
    return queryString ? `${fullURL}?${queryString}` : fullURL;
  }

  /**
   * 处理响应
   */
  async handleResponse(response, config) {
    // 如果显示了loading，需要隐藏
    if (config.showLoading) {
      this.count--;
    }

    // 执行响应拦截器
    const processedResponse = await this.executeResponseInterceptors(
      response,
      config
    );

    if (!processedResponse.ok) {
      const error = new Error(
        `HTTP error! status: ${processedResponse.status}`
      );
      error.status = processedResponse.status;
      error.statusText = processedResponse.statusText;

      try {
        const errorData = await processedResponse.json();
        error.data = errorData;
      } catch {
        // 忽略JSON解析错误
      }

      throw error;
    }

    // 检查响应是否为空
    const contentType = processedResponse.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      return await processedResponse.json();
    }

    return await processedResponse.text();
  }

  /**
   * 通用请求方法
   */
  async request(url, config) {
    // 处理showLoading参数
    if (config.showLoading) {
      this.count++;
    }

    try {
      // 执行请求拦截器
      const processedConfig = await this.executeRequestInterceptors(config);

      // 发送请求
      const response = await fetch(url, processedConfig);

      // 处理响应
      return await this.handleResponse(response, processedConfig);
    } catch (error) {
      // 确保在出错时隐藏loading
      if (config.showLoading) {
        this.count--;
      }
      throw error;
    }
  }

  /**
   * GET请求
   * @param {string} url - 请求URL
   * @param {object} params - 查询参数
   * @param {object} options - 额外的fetch选项，包括showLoading
   */
  async get(url, params = null, options = {}) {
    const fullURL = this.buildURL(url, params);

    const config = {
      method: "GET",
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      ...options,
    };

    return this.request(fullURL, { ...config, ...options });
  }

  /**
   * POST请求
   * @param {string} url - 请求URL
   * @param {object} data - 请求体数据
   * @param {object} options - 额外的fetch选项，包括showLoading
   */
  async post(url, data = {}, options = {}) {
    let config = {
      method: "POST",
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    };

    const isFormData = data instanceof FormData;
    if (isFormData) {
      config = {
        method: "POST",
        headers: {
          ...options.headers,
        },
        body: data,
        ...options,
      };
    }

    return this.request(this.baseURL + url, { ...config, ...options });
  }

  /**
   * PUT请求
   * @param {string} url - 请求URL
   * @param {object} data - 请求体数据
   * @param {object} options - 额外的fetch选项，包括showLoading
   */
  async put(url, data = null, options = {}) {
    const config = {
      method: "PUT",
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    };

    return this.request(this.baseURL + url, { ...config, ...options });
  }

  /**
   * DELETE请求
   * @param {string} url - 请求URL
   * @param {object} params - 查询参数或请求体数据
   * @param {object} options - 额外的fetch选项，包括showLoading
   */
  async delete(url, params = null, options = {}) {
    let fullURL = this.baseURL + url;
    let config = {
      method: "DELETE",
      redirect: "follow",
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "include",
      mode: "cors",
      ...options,
    };

    // 判断params是否应该作为查询参数或请求体
    if (params && typeof params === "object" && !Array.isArray(params)) {
      // 如果params是普通对象，检查是否应该作为查询参数
      const isQueryParams =
        Object.keys(params).length === 1 &&
        (Object.prototype.hasOwnProperty.call(params, "id") ||
          Object.prototype.hasOwnProperty.call(params, "ids"));

      if (isQueryParams) {
        fullURL = this.buildURL(url, params);
      } else {
        // 作为请求体发送
        config.body = JSON.stringify(params);
      }
    } else if (Array.isArray(params)) {
      // 数组形式的数据作为请求体发送
      config.body = JSON.stringify(params);
    } else if (params) {
      // 其他情况作为查询参数
      fullURL = this.buildURL(url, { id: params });
    }

    return this.request(fullURL, { ...config, ...options });
  }

  /**
   * 下载文件
   * @param {string} url - 请求URL
   * @param {object} params - 查询参数
   * @param {string} filename - 下载文件名
   * @param {object} options - 额外的fetch选项，包括showLoading
   */
  async download(url, params = null, filename = "download", options = {}) {
    const fullURL = this.buildURL(url, params);

    const config = {
      method: "GET",
      ...options,
    };

    // 执行请求拦截器
    const processedConfig = await this.executeRequestInterceptors(config);

    const response = await fetch(fullURL, processedConfig);

    // 执行响应拦截器
    const processedResponse = await this.executeResponseInterceptors(
      response,
      processedConfig
    );

    if (!processedResponse.ok) {
      throw new Error(`HTTP error! status: ${processedResponse.status}`);
    }

    const blob = await processedResponse.blob();

    // 创建下载链接
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = downloadUrl;

    // 尝试从响应头获取文件名
    const disposition = processedResponse.headers.get("Content-Disposition");
    if (disposition && disposition.includes("filename=")) {
      const filenameMatch = disposition.match(
        /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
      );
      if (filenameMatch) {
        filename = filenameMatch[1].replace(/['"]/g, "");
      }
    }

    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // 清理URL对象
    window.URL.revokeObjectURL(downloadUrl);

    return blob;
  }
}

// 创建默认实例
const request = new Request();

// 添加默认请求拦截器 - Token处理
request.addRequestInterceptor((config, options) => {
  const token =
    localStorage.getItem("token") || sessionStorage.getItem("token");
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

// 添加默认响应拦截器 - 错误处理
request.addResponseInterceptor((response, config) => {
  // 可以在这里添加全局错误处理逻辑
  // 比如token过期自动跳转登录页等
  return response;
});

// 导出方法
export const get = request.get.bind(request);
export const post = request.post.bind(request);
export const put = request.put.bind(request);
export const del = request.delete.bind(request);
export const download = request.download.bind(request);

// 导出类，允许创建自定义实例
export { Request };

// 默认导出
export default request;
