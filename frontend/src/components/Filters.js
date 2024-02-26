import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Paper, Box, Button, Grid } from "@mui/material";

import { setAccountFilter } from "../Redux/slices/accountFilterSlice";
import { setActivityTypeFilter } from "../Redux/slices/activityTypeFilterSlice";

import MultipleSelectCheckmarks from "./SelectCheckmark";

const Filters = ({ activityTypes }) => {
  const dispatch = useDispatch();

  const [selectedAccounts, setSelectedAccounts] = useState([]);
  const [selectedActivityTypes, setSelectedActivityTypes] = useState([]);
  const storeAccounts = useSelector((state) => state.accounts.value);

  const onFilterFunction = (event) => {
    const selectedAccountNumbers = [];

    selectedAccounts.forEach((selectedAccount) => {
      const accountNumber = storeAccounts
        .filter((storeAccount) => storeAccount.label === selectedAccount)
        .map((account) => account.account_number)[0];
      selectedAccountNumbers.push(accountNumber);
    });

    dispatch(setAccountFilter(selectedAccountNumbers));
    dispatch(setActivityTypeFilter(selectedActivityTypes));
  };

  return (
    <Box
      style={{
        width: "100%",
      }}
    >
      <Paper sx={{ p: 1 }}>
        <Grid container spacing={2} display={"flex"} justifyContent={"center"}>
          <Grid item>
            {activityTypes.length > 0 ? (
              <MultipleSelectCheckmarks
                data={activityTypes}
                selectedFilters={selectedActivityTypes}
                setter={setSelectedActivityTypes}
                label="Activity Types"
              />
            ) : (
              <div></div>
            )}
          </Grid>
          <Grid item>
            {storeAccounts.length > 0 ? (
              <MultipleSelectCheckmarks
                data={storeAccounts}
                selectedFilters={selectedAccounts}
                setter={setSelectedAccounts}
                label="Accounts"
              />
            ) : (
              <div></div>
            )}
          </Grid>
          <Grid display="flex" alignItems="center" item>
            <Button
              variant="contained"
              size="medium"
              onClick={() => onFilterFunction()}
            >
              Filter
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default Filters;
