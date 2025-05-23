import { provideRouter } from '@angular/router';
import { appRoutes } from './app.routes';  // Import the routes form the app.routes.ts file

export const appConfig = {
  providers: [
    provideRouter(appRoutes)  // Give the routes to the router
  ]
};
