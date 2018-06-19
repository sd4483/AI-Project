package sg.gowild.sademo;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Environment;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.apache.http.conn.ConnectTimeoutException;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.TimeUnit;

import ai.api.AIConfiguration;
import ai.api.AIDataService;
import ai.api.AIServiceException;
import ai.api.model.AIRequest;
import ai.api.model.AIResponse;
import ai.api.model.Fulfillment;
import ai.api.model.Result;
import ai.kitt.snowboy.SnowboyDetect;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    // View Variables
    private Button button;
    private TextView textView;
    String text = "";
    String text1 = "";
    String SYMPTOMS_RESPONSES []= {"You are likely to suffer from Dengue virus", "you are likely to suffer from malaria", "you are likely to suffer from zika", "you are likely to suffer from viral fever", "you are likely to suffer from typhoid"};
    // ASR Variables
    private SpeechRecognizer speechRecognizer;

    // TTS Variables
    private TextToSpeech textToSpeech;

    // NLU Variables
    private AIDataService aiDataService;

    // Hotword Variables
    private boolean shouldDetect;
    private SnowboyDetect snowboyDetect;

    static {
        System.loadLibrary("snowboy-detect-android");
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // TODO: Setup Components
        setupViews();
        setupXiaoBaiButton();
        setupAsr();
        setupTts();
        setupNlu();
        setupHotword();

        // TODO: Start Hotword
        startHotword();
    }

    private void setupViews() {
        // TODO: Setup Views
        button = findViewById(R.id.button);
        textView = findViewById(R.id.textview);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                startAsr();
            }
        });
    }

    private void setupXiaoBaiButton() {
        String BUTTON_ACTION = "com.gowild.action.clickDown_action";

        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(BUTTON_ACTION);

        BroadcastReceiver broadcastReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                // TODO: Add action to do after button press is detected

                startAsr();
            }
        };
        registerReceiver(broadcastReceiver, intentFilter);
    }

    private void setupAsr() {
        // TODO: Setup ASR
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle bundle) {

            }

            @Override
            public void onBeginningOfSpeech() {

            }

            @Override
            public void onRmsChanged(float v) {

            }

            @Override
            public void onBufferReceived(byte[] bytes) {

            }

            @Override
            public void onEndOfSpeech() {

            }

            @Override
            public void onError(int i) {
                Log.e("asr","Error: "+Integer.toString(i));
                startHotword();
            }

            @Override
            public void onResults(Bundle results) {
                List<String> texts = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if(texts == null || texts.isEmpty()){
                    textView.setText("Pls try again");
                }
                else {
                    text = texts.get(0);
                    textView.setText(text);

                    startNlu(text);
                }
            }

            @Override
            public void onPartialResults(Bundle bundle) {

            }

            @Override
            public void onEvent(int i, Bundle bundle) {

            }
        });
    }

    private void startAsr() {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                // TODO: Set Language
                final Intent recognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "EN");
                recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "EN");
                recognizerIntent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, getPackageName());
                recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_WEB_SEARCH);
                recognizerIntent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3);

                // Stop hotword detection in case it is still running
                shouldDetect = false;

                // TODO: Start ASR
                speechRecognizer.startListening(recognizerIntent);
            }
        };
        Threadings.runInMainThread(this, runnable);
    }

    private void setupTts() {
        // TODO: Setup TTS
        textToSpeech = new TextToSpeech(this,null);
    }

    private void startTts(String text) {
        // TODO: Start TTS
        textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH,null);

        // TODO: Wait for end and start hotword
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                while (textToSpeech.isSpeaking()) {
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Log.e("tts", e.getMessage(), e);
                    }
                }

                startHotword();
            }
        };
        Threadings.runInBackgroundThread(runnable);
    }

    private void setupNlu() {
        // TODO: Change Client Access Token
        String clientAccessToken = "ba65838778f2425fa39fe5d3b9ab56b9";
        AIConfiguration aiConfiguration = new AIConfiguration(clientAccessToken,
                AIConfiguration.SupportedLanguages.English);
        aiDataService = new AIDataService(aiConfiguration);
    }

    private void startNlu(final String text) {
        // TODO: Start NLU
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                AIRequest aiRequest = new AIRequest();
                System.out.println("startNlu: " + text);
                aiRequest.setQuery(text);
                try {
                    AIResponse aiResponse = aiDataService.request(aiRequest);

                    Result result = aiResponse.getResult();
                    Fulfillment fulfillment = result.getFulfillment();
                    String responseText = fulfillment.getSpeech();

                    if(responseText.equalsIgnoreCase("weather_function")) {
                        responseText = getWeather();
                    }
                    else if(responseText.equalsIgnoreCase("sick")) {
                        responseText = sick();
                    }
                    else if(responseText.equalsIgnoreCase("symptoms")) {
                        text1 += text.replace(" ", "_" );
                        text1 = text1+"_";
                        responseText = symptoms();
                    }
                    else if(responseText.equalsIgnoreCase("more_symp")) {
                        responseText = more_symp();
                    }
                    startTts(responseText);
                }
                catch (AIServiceException e){
                    Log.e("nlu", e.getMessage(), e);
                }
            }
        };
        Threadings.runInBackgroundThread(runnable);
    }

    private void setupHotword() {
        shouldDetect = false;
        SnowboyUtils.copyAssets(this);

        // TODO: Setup Model File
        File snowboyDirectory = SnowboyUtils.getSnowboyDirectory();
        File model = new File(snowboyDirectory, "alexa_02092017.umdl");
        File common = new File(snowboyDirectory, "common.res");

        // TODO: Set Sensitivity
        snowboyDetect = new SnowboyDetect(common.getAbsolutePath(), model.getAbsolutePath());
        snowboyDetect.setSensitivity("0.60");
        snowboyDetect.applyFrontend(true);
    }

    private void startHotword() {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                shouldDetect = true;
                android.os.Process.setThreadPriority(android.os.Process.THREAD_PRIORITY_AUDIO);

                int bufferSize = 3200;
                byte[] audioBuffer = new byte[bufferSize];
                AudioRecord audioRecord = new AudioRecord(
                        MediaRecorder.AudioSource.DEFAULT,
                        16000,
                        AudioFormat.CHANNEL_IN_MONO,
                        AudioFormat.ENCODING_PCM_16BIT,
                        bufferSize
                );

                if (audioRecord.getState() != AudioRecord.STATE_INITIALIZED) {
                    Log.e("hotword", "audio record fail to initialize");
                    return;
                }

                audioRecord.startRecording();
                Log.d("hotword", "start listening to hotword");

                while (shouldDetect) {
                    audioRecord.read(audioBuffer, 0, audioBuffer.length);

                    short[] shortArray = new short[audioBuffer.length / 2];
                    ByteBuffer.wrap(audioBuffer).order(ByteOrder.LITTLE_ENDIAN).asShortBuffer().get(shortArray);

                    int result = snowboyDetect.runDetection(shortArray, shortArray.length);
                    if (result > 0) {
                        Log.d("hotword", "detected");
                        shouldDetect = false;
                    }
                }

                audioRecord.stop();
                audioRecord.release();
                Log.d("hotword", "stop listening to hotword");

                // TODO: Add action after hotword is detected
                startAsr();
            }
        };
        Threadings.runInBackgroundThread(runnable);
    }

    private String getWeather() {
        // TODO: (Optional) Get Weather Data via REST API

        OkHttpClient okHttpClient = new OkHttpClient();
        Request request = new Request.Builder()
                .url("https://api.data.gov.sg/v1/environment/2-hour-weather-forecast")
                .addHeader("accept", "application/json")
                .build();

        try {
            Response response = okHttpClient.newCall(request).execute();
            String responseBody = response.body().string();

            JSONObject jsonObject = new JSONObject(responseBody);
            JSONArray forecasts = jsonObject.getJSONArray("items")
                    .getJSONObject(0)
                    .getJSONArray("forecasts");

            for(int i = 0; i < forecasts.length(); i++){
                JSONObject forecastObject = forecasts.getJSONObject(i);
                String area = forecastObject.getString("area");

                if(area.equalsIgnoreCase("clementi")){
                    String forecast = forecastObject.getString("forecast");
                    return "the weather in clementi is now "+forecast;
                }

            }
        }
        catch (IOException e) {
            Log.e("weather", e.getMessage(),e);
        }
        catch (JSONException e) {
            Log.e("weather", e.getMessage(),e);
        }
        return "No weather info";
    }



    private String sick() {
        // TODO: (Optional) Get Weather Data via REST API
        try {
        OkHttpClient okHttpClient = new OkHttpClient();
        Request request = new Request.Builder()
                .url("http://127.0.0.1:5000/sick")
                .build();


            Response response = okHttpClient.newCall(request).execute();
            String responseBody = response.body().string();

            JSONObject jsonObject = new JSONObject(responseBody);
            JSONArray forecasts = jsonObject
                                    .getJSONArray("items");



                JSONObject forecastObject = forecasts.getJSONObject(0);
                String area = forecastObject.getString("a");

                if(area.equalsIgnoreCase("one")){
                    String forecast = forecastObject.getString("message");
                    return forecast;
                }





        }
        catch (IOException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  IO sick()");
        }
        catch (JSONException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  JSON sick()");
        }
        catch (Exception e){
            System.out.println(e.getMessage()+ "     ---->  sick()");
        }
        return "Sorry technical difficulties faced. Please try again later.";
    }

    private String symptoms() {
        // TODO: (Optional) Get Weather Data via REST API
        try {
            System.out.println(text1);
            OkHttpClient okHttpClient = new OkHttpClient();
            Request request = new Request.Builder()
                    .url("http://127.0.0.1:5000/symptoms/"+text1)
                    .build();


            Response response = okHttpClient.newCall(request).execute();
            String responseBody = response.body().string();

            JSONObject jsonObject = new JSONObject(responseBody);
            JSONArray forecasts = jsonObject
                    .getJSONArray("items");



                JSONObject forecastObject = forecasts.getJSONObject(0);
                String area = forecastObject.getString("a");

                if(area.equalsIgnoreCase("one")){
                    String forecast = forecastObject.getString("message");
                    for(int j = 0; j < SYMPTOMS_RESPONSES.length; j++)
                    {
                        if(SYMPTOMS_RESPONSES[j].equalsIgnoreCase(forecast))
                        {
                            text1 = "";
                            return forecast;
                        }
                    }
                    return forecast;
                }





        }
        catch (IOException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  IO symptom()");
        }
        catch (JSONException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  JSON symptom()");
        }
        catch (Exception e){
            System.out.println(e.getMessage()+ "     ---->  symptom()");
        }
        return "Sorry technical difficulties faced. Please try again later.";
    }


    private String more_symp() {
        // TODO: (Optional) Get Weather Data via REST API
        try {
            OkHttpClient okHttpClient = new OkHttpClient();

            Request request = new Request.Builder()
                    .url("http://127.0.0.1:5000/more_symp/"+text)
                    .build();


            Response response = okHttpClient.newCall(request).execute();
            String responseBody = response.body().string();

            JSONObject jsonObject = new JSONObject(responseBody);
            JSONArray forecasts = jsonObject
                    .getJSONArray("items");



                JSONObject forecastObject = forecasts.getJSONObject(0);
                String area = forecastObject.getString("a");

                if(area.equalsIgnoreCase("one")){
                    String forecast = forecastObject.getString("message");
                    return forecast;
                }
        }
        catch (IOException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  IO symptom()");
        }
        catch (JSONException e) {
            Log.e("weather", e.getMessage(),e);
            System.out.println(e.getMessage()+ "     ---->  JSON symptom()");
        }
        catch (Exception e){
            System.out.println(e.getMessage()+ "     ---->  symptom()");
        }
        return "Sorry technical difficulties faced. Please try again later.";
    }
}
