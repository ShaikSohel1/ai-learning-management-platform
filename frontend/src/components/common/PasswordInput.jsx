import React, { useState } from "react";
import { Lock, Eye, EyeOff } from "lucide-react";

export function PasswordInput({
  label = "Password",
  value,
  onChange,
  placeholder = "••••••••",
  required = true,
  name = "password",
  id,
}) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="login-input-group">
      {label && <label htmlFor={id || name}>{label}</label>}
      <div className="login-input-box" style={{ position: "relative" }}>
        <Lock size={18} color="var(--text-muted)" />
        <input
          id={id || name}
          name={name}
          type={showPassword ? "text" : "password"}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required={required}
          style={{ paddingRight: "40px" }}
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          style={{
            position: "absolute",
            right: "12px",
            background: "none",
            border: "none",
            color: "var(--text-muted)",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            padding: "4px",
          }}
          aria-label={showPassword ? "Hide password" : "Show password"}
        >
          {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
    </div>
  );
}

export default PasswordInput;
