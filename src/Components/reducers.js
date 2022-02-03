const data = {
    data1: {},
    data2: {},
    full_data1: {},
    dict_dataa1: {},
    dict_1: {},
    dict: {},
    state: "",
  };
  
  export default function mainReducer(state = data, action) {
    switch (action.type) {
      case 'SET_DATA':
        return Object.assign({}, state, {
            data1: action.data1
        });
        case 'SET_DATA_1':
        return Object.assign({}, state, {
            data2: action.data2
        });
        case 'SET_FULL_DATA':
        return Object.assign({}, state, {
            full_data1: action.full_data1
        });
      case 'SET_DICT_DATAA':
        return Object.assign({}, state, {
            dict_dataa1: action.dict_dataa1
        });
      case 'SET_DICT_1':
        return Object.assign({}, state, {
            dict_1: action.dict_1
        });
      case 'SET_DICT':
        return Object.assign({}, state, {
            dict: action.dict
        });
      case 'SET_STATE':
        return Object.assign({}, state, {
            state: action.state
        });
      
      default:
        return state;
    }
  }