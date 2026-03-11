package com.testadapter.configurations;

import com.testadapter.utils.TestApplication;
import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

@CucumberContextConfiguration
@SpringBootTest(classes = TestApplication.class)
public class CucumberSpringConfiguration {

    @io.cucumber.java.Before
    public void setUp() {
        // Configuration setup before each scenario
    }
}
