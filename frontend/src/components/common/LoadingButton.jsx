import React from "react";
import Button from "./Button";

export function LoadingButton({
  children,
  loading = false,
  loadingText = "Processing...",
  disabled = false,
  ...props
}) {
  return (
    <Button
      disabled={disabled || loading}
      loading={loading}
      {...props}
    >
      {loading ? loadingText : children}
    </Button>
  );
}

export default LoadingButton;
