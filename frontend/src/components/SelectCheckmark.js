import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};


const MultipleSelectCheckmarks = ({data})  => {

  const [selectedVal, setSelectedVal] = React.useState([]);
    
  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedVal(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">Tag</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={selectedVal}
          onChange={handleChange}
          input={<OutlinedInput label="Tag" />}
          renderValue={(selected) => selected.join(', ')}
          MenuProps={MenuProps}
        >
            {
                console.log(data)
                
            }
          { (data.length > 0) ?
             data.map((obj) => (
                <MenuItem key={obj.label + obj.accountNumber} value={obj.label}>
                  <Checkbox checked={selectedVal.indexOf(obj.label) > - 1} />
                  <ListItemText primary={obj.label} />
                </MenuItem>
              )) : <MenuItem>
                None
            </MenuItem>
        }
        </Select>
      </FormControl>
    </div>
  );
}

export default  MultipleSelectCheckmarks;