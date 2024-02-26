import * as React from "react";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import ListItemText from "@mui/material/ListItemText";
import Select from "@mui/material/Select";
import Checkbox from "@mui/material/Checkbox";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 200,
    },
  },
};

const MultipleSelectCheckmarks = ({ data, selectedFilters, setter, label }) => {
  const handleChange = (event) => {
    let {
      target: { value },
    } = event;
    if (data[0].account_number) {
      const accountNumber = data.reduce((entry) =>
        entry.label == value ? entry.account_number : ""
      );
    }
    const val = setter(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">{label}</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={selectedFilters}
          onChange={handleChange}
          input={<OutlinedInput label="Tag" />}
          renderValue={(selected) => selected.join(", ")}
          MenuProps={MenuProps}
        >
          {data.length > 0 ? (
            data.map((obj) => (
              <MenuItem
                key={obj.label + obj.accountNumber}
                value={obj.label}
                accountnumber={obj.account_number ? obj.account_number : ""}
              >
                <Checkbox checked={selectedFilters.indexOf(obj.label) > -1} />
                <ListItemText primary={obj.label} />
              </MenuItem>
            ))
          ) : (
            <MenuItem>None</MenuItem>
          )}
        </Select>
      </FormControl>
    </div>
  );
};

export default MultipleSelectCheckmarks;
