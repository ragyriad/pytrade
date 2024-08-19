import React, { useRef } from "react";
import { setCsrfToken, setWsRefreshToken } from "../../Redux/slices/authSlice";
import { useSelector, useDispatch } from "react-redux";
import { Paper } from "@mui/material";
import {
  Modal,
  ModalClose,
  ModalDialog,
  DialogTitle,
  DialogContent,
  Stack,
  FormControl,
  Input,
  Button,
} from "@mui/joy";

const WealthsimpleModal = ({ status, modalAction }) => {
  let inputRef = useRef(null);
  const dispatch = useDispatch();
  const csrftoken = useSelector((state) => state.auth.csrfToken.value);

  const sendAuthCode = (event) => {
    event.preventDefault();
    const authCode = inputRef.current.value;
    const host = window.location.origin;
    const options = {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      mode: "same-origin",
      body: authCode,
    };
    fetch(host + "/api/wealthsimple/auth", options)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        dispatch(setWsRefreshToken(data["Token"]));
        const refreshToken = useSelector(
          (state) => state.auth.wsRefreshToken.value
        );
        console.log("Refresh Token " + refreshToken);
        modalAction(false);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <Modal
      open={status}
      onClose={() => modalAction(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Paper>
        <ModalDialog>
          <ModalClose variant="plain" sx={{ m: 1 }} />
          <DialogTitle>Authentication</DialogTitle>
          <DialogContent>Please Enter Your 2FA Code</DialogContent>
          <form onSubmit={sendAuthCode}>
            <Stack spacing={2}>
              <FormControl>
                <Input
                  slotProps={{
                    input: {
                      ref: inputRef,
                    },
                  }}
                  autoFocus
                  required
                />
              </FormControl>
              <Button type="submit">Submit</Button>
            </Stack>
          </form>
        </ModalDialog>
      </Paper>
    </Modal>
  );
};

export default WealthsimpleModal;
