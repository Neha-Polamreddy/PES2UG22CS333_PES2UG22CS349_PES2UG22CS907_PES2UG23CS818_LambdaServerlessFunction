exports.handler = async (event) => {
  return { message: `Hello, ${event.name || 'World'} from Node.js!` };
};
