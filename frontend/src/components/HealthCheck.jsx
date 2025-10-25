// src/components/HealthCheck.jsx
import React, {useEffect, useState} from "react";
import { api } from "../lib/api";
import { Button, Typography } from "@mui/material";

export default function HealthCheck(){
  const [status, setStatus] = useState("unknown");

  const check = async () => {
    try {
      const res = await api.get("/");
      setStatus("OK: " + (res.data?.message || "running"));
    } catch (e) {
      setStatus("Error: " + (e.message || "no connection"));
    }
  };

  useEffect(()=>{ check() }, []);
  return (
    <div style={{marginTop: 16}}>
      <Button variant="outlined" onClick={check}>Check Backend</Button>
      <Typography variant="body2" sx={{mt:1}}>{status}</Typography>
    </div>
  );
}