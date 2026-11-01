import ReactDOM from 'react-dom';
const Post = (props) => <p>{props.x}</p>;
Post.getInitialProps = ({ query }) => ({ x: query.id });
export default Post;
