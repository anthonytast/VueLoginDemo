
const clearForm = (...args) => {
    args.forEach(arg => {
        arg.value = ""
    })
}

export default clearForm;