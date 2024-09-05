import React, { useState } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { Grid, Button, Paper, Snackbar } from "@mui/material";
import WealthsimpleAuthModal from "../Modals/WealthsimpleAuthModal";

const fetchData = async (refreshToken, csrfToken, account_id = null) => {
  try {
    let syncActivitiesUrl = new URL(
      "http://localhost:8000/api/wealthsimple/activity"
    );
    const data = {
      refreshToken: refreshToken,
      account_id: account_id,
    };
    const response = await axios({
      method: "POST",
      url: syncActivitiesUrl,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      data,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      const status = error.response.status;
      const message = error.response.data.error_message || "An error occurred";
      throw { status, message }; // Throw an object with status and message
    } else {
      // Handle errors where error.response does not exist
      throw { status: 500, message: "Network Error" }; // Generic error message
    }
  }
};

const UpdatePage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMsg, setSnackbarMsg] = useState(null);

  let refreshToken = useSelector((state) => state.auth.wsRefreshToken);
  let csrfToken = useSelector((state) => state.auth.csrfToken);

  const handleModalClose = () => {
    setModalOpen(false);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const handleMfaSubmit = async (mfaCode) => {
    try {
      console.log("in MFA Submit" + mfaCode);
      setLoading(true);
      const result = await fetchData(refreshToken, csrfToken, null, mfaCode);
      setData(result);
      setError(null);
      setModalOpen(false);
    } catch (error) {
      console.log("Update Page Error");
      console.log(error);
      setError(error.message);
      if (error.status === 401) {
        // If there's a 401 error, open the modal and set the error message
        // Set the error message from the response
        setModalOpen(true);
      } else if (error.status === 400) {
        setError("MFA Code is incorrect, please try again.");
        setModalOpen(true);
      } else {
        console.log("Handle Error");
        console.log(error.message);
        setSnackbarOpen(true);
      }
    } finally {
      setLoading(false);
    }
  };

  const updateBroker = async (Broker) => {
    if (Broker === "Wealthsimple") {
      setLoading(true);
      try {
        await fetchData(refreshToken, csrfToken, null);
        setSnackbarOpen(true); // Show snackbar after request is sent
      } catch (error) {
        console.log("Update Page Error");
        console.log(error);
        setError(error.message);
        if (error.status === 401) {
          setModalOpen(true);
        } else if (error.status === 400) {
          setError("MFA Code is incorrect, please try again.");
          setModalOpen(true);
        } else {
          console.log("Handle Error");
          console.log(error.message);
          setSnackbarOpen(true);
        }
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Grid>
      <WealthsimpleAuthModal
        open={modalOpen}
        handleClose={handleModalClose}
        handleSubmit={handleMfaSubmit}
        errorMessage={error}
      />
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        message={snackbarMsg}
      />
      <Paper sx={{ p: 2 }}>
        <Grid container spacing={2} justifyContent={"center"}>
          <Grid item>
            <Button
              variant="contained"
              size="medium"
              onClick={() => updateBroker("Questrade")}
            >
              Questrade
            </Button>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              size="medium"
              onClick={() => updateBroker("Wealthsimple")}
            >
              Wealthsimple
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Grid>
  );
};

export default UpdatePage;
