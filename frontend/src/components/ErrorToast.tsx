import { Toast, ToastContainer } from "react-bootstrap";

interface IErrorToastProps {
  show: boolean;
  setShow: (value: boolean) => void;
  reason: Error;
}

function ErrorToast({ show, setShow, reason }: IErrorToastProps) {
  return (
    <ToastContainer className="p-1" position="bottom-end" style={{ zIndex: 1 }}>
      <Toast
        onClose={() => setShow(false)}
        bg="dark"
        show={show}
        delay={3000}
        autohide
      >
        <Toast.Header>
          <small className="me-auto">Error!</small>
        </Toast.Header>
        <Toast.Body className="text-white">
          <small>{reason.name + ": " + reason.message}</small>
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

export default ErrorToast;
