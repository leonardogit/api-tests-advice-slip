package com.testadapter.properties;

import org.aeonbits.owner.Config;

@Config.Sources({"classpath:conf/${ENVIRONMENT}.properties"})
public interface PropertiesConfiguration extends Config {

    @Key("env.base_url")
    String baseUrl();
}
