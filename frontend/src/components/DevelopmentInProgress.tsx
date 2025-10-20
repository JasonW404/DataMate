import { Button } from "antd";

const DevelopmentInProgress = ({ showHome = true }) => {
  return (
    <div className="mt-40 flex flex-col items-center justify-center">
      <div className="hero-icon">🚧</div>
      <h1 className="text-2xl font-bold">功能开发中</h1>
      <p className="mt-4">我们正在全力开发新功能，为您带来更好的体验</p>
      {showHome && (
        <Button
          type="primary"
          className="mt-6"
          onClick={() => {
            window.location.href = "/";
          }}
        >
          返回首页
        </Button>
      )}
    </div>
  );
};

export default DevelopmentInProgress;
