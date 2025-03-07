import { Snackbar } from "@mui/material";

const Snackbar = (message) => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMsg, setSnackbarMsg] = useState(null);
  setSnackbarMsg(setSnackbarMsg);

  return (
    <Snackbar
      open={snackbarOpen}
      autoHideDuration={3000}
      onClose={setSnackbarOpen(false)}
      message={snackbarMsg}
    />
  );
};

export default Snackbar;
