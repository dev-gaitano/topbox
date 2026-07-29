import { ToastProps } from "../../../props";

function SuccessToast({ title, subtext }: ToastProps) {
  return (
    <div className="success-toast" role="status">
      <div>
        <p className="success-toast-title">{title}</p>
        <p className="success-toast-subtext">{subtext}</p>
      </div>
    </div>
  );
}

export default SuccessToast;
