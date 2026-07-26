import React from "react";
import { motion } from "framer-motion";

export function Card({ children, className = "", style = {}, onClick }) {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className={`glass-card ${className}`}
      style={{
        padding: "24px",
        ...style,
      }}
    >
      {children}
    </motion.div>
  );
}

export default Card;
