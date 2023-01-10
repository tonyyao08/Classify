// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { Image, Project } = initSchema(schema);

export {
  Image,
  Project
};