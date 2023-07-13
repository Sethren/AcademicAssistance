# Dojo-Blog

## Description
- project uses react to create a website that can take blogs
- blogs are written and stored real time in json files

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Installation Instructions:
- run `npm install` to install the node_modules folder which contains the dependencies located in package.json

- run `npm install react-router-dom@5.2.0` to install react router

- on a new terminal run `npx json-server --watch data/db.json --port 8000` to start a json server for the db.json file located in data folder

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

npx json-server --watch data/db.json --port 8000

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)


# Role of Each file
# App.js:
- contains all the pages for the website
- uses react router dom v5 to switch pages
- contains Home, Create, BlogDetails, and NotFound pages
# BlogDetails.js:
- contains all the details such as suthor, paragraph, and title on the page
- also contains the delete function to remove the blog from db.json and from the website
# BlogList.js:
- Takes all the blogs and formats them containing title and author
- Blogs are all linked to a specific page depending on their blog id
- the link takes you to the BlogDetails page which opens the blog details and is formed based on id
# Create.js:
- used to create a blog and add
- includes details, such as content, author, and title
- once blog is created, it is added to the db.json file which means that it's stored
# Home.js:
- the home page for the website
- contains all the blogs here
- uses UseFetch to json request the blogs
- blogs are sent to BlogList where they are formatted and returned
# index.css: 
- contains all the fonts and colors for the
# index.js: 
- this is where App.js is run and the render function occurs
- this is where the index.css is applied which goes onto the other files
# Navbar.js:
- this is stored in the App.js file and is in all pages
- Links to the create and the home page
# NotFound.js:
- this file is the Not Found page is the user tries to acces a page that has not been created
# useFetch.js:
- this file makes the json request for data from the db.json file in the data folder
- the file returns data, isPending, and error
- data contains data and isPending and error return something other than null is there's an error with the request