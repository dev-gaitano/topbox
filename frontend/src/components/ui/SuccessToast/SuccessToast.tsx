import { ToastProps } from "../../../props";
import "./SuccessToast.css";

function getToastClass(success: string) {
  if (success === "green") return "toast--success";
  if (success === "red") return "toast--error";
  if (success === "info") return "toast--info";
  return "";
}
function SuccessToast({ title, subtext, success }: ToastProps) {
  return (
    <div className={`success-toast ${getToastClass(success)}`} role="status">
      <div>
        <p className="success-toast-title">{title}</p>
        <p className="success-toast-subtext">{subtext}</p>
      </div>
    </div>
  );
}

export default SuccessToast;
