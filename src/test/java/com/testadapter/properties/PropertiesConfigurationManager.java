package com.testadapter.properties;

import org.aeonbits.owner.ConfigCache;
import org.aeonbits.owner.ConfigFactory;

public class PropertiesConfigurationManager {

    private static final String ENVIRONMENT = "ENVIRONMENT";

    public static PropertiesConfiguration getProperties() {
        setEnvironment();
        return ConfigCache.getOrCreate(PropertiesConfiguration.class);
    }

    private static void setEnvironment() {
        String environment = System.getenv(ENVIRONMENT);
        String actualEnv = environment == null ? "dev" : environment;

        System.setProperty(ENVIRONMENT, actualEnv);
        ConfigFactory.setProperty(ENVIRONMENT, actualEnv);
    }
}
