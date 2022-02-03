export function setData(data1) {
	return {
		type: 'SET_DATA',
		data1: data1
	};
}

export function setDictDataa(dict_dataa1) {
  return {
    type: 'SET_DICT_DATAA',
    dict_dataa1: dict_dataa1
  };
}

export function setData1(data2) {
    return {
      type: 'SET_DATA_1',
      data2: data2
    };
}

export function setFullData(full_data1) {
    return {
      type: 'SET_FULL_DATA',
      full_data1: full_data1
    };
  }

export function setDict_1(dict_1) {
  return {
    type: 'SET_DICT_1',
    dict_1: dict_1
  };
}

export function setDict(dict) {
  return {
    type: 'SET_DICT',
    dict: dict
  };
}

export function setState(state) {
  return {
    type: 'SET_STATE',
    state: state
  };
}

// export function setImpact(origI) {
//   return {
//     type: 'SET_IMPACT',
//     origI: origI
//   };
// }

export function TitlebarGridList(){
    return function thunk(dispatch){

    }, function(data){
        //dispatch(setState(data))
    }
}