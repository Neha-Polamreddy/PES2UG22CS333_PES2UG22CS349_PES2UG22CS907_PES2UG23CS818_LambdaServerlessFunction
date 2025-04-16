// user_function/user_function/2/function.js

exports.handler = (event) => {
  return { message: `Hello, ${event.name || "World"}!` };
};
