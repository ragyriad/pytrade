import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button } from "@mui/material";

const WealthsimpleAuthModal = ({
  open,
  handleClose,
  handleAuthSubmit,
  errorMessage,
}) => {
  const [otp, setOtp] = useState("");

  const handleOtpChange = (event) => {
    setOtp(event.target.value);
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 400,
          bgcolor: "background.paper",
          boxShadow: 24,
          p: 4,
        }}
      >
        <Typography variant="h6" component="h2">
          Enter 2FA Code
        </Typography>
        {errorMessage && (
          <Typography color="error" variant="body2">
            {errorMessage}
          </Typography>
        )}
        <TextField
          label="2FA Code"
          variant="outlined"
          fullWidth
          margin="normal"
          value={otp}
          onChange={handleOtpChange}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={() => {
            handleAuthSubmit(otp);
            handleClose();
          }}
        >
          Submit
        </Button>
      </Box>
    </Modal>
  );
};

export default WealthsimpleAuthModal;
